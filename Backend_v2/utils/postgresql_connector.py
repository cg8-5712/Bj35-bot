import hashlib
import logging
import asyncio
from asyncio import Lock
from typing import Dict, Optional, Any

import asyncpg

from settings import settings

class PostgreSQLConnector:
    """PostgreSQL 数据库连接管理类，提供数据库操作的各种方法。"""
    pool: Optional[asyncpg.Pool] = None
    lock: Lock = Lock()  # 创建一个全局锁

    @classmethod
    async def initialize(cls) -> None:
        """初始化数据库连接池"""
        if cls.pool:
            logging.info("数据库连接池已存在，跳过初始化")
            return

        max_retries = 3
        retry_count = 0

        while retry_count < max_retries:
            try:
                # 创建连接池
                cls.pool = await asyncpg.create_pool(
                    user=settings.DB_USER,
                    password=settings.DB_PASSWORD,
                    database=settings.DB_NAME,
                    host=settings.DB_HOST,
                    port=settings.DB_PORT,
                    min_size=settings.DB_POOL_MIN_SIZE,
                    max_size=settings.DB_POOL_MAX_SIZE,
                    ssl=settings.DB_SSL,
                    timeout=60,  # 设置连接超时时间
                    command_timeout=60,  # 设置命令超时时间
                    max_inactive_connection_lifetime=300,  # 设置最大非活动连接生命周期
                    max_lifetime=3600,  # 设置最大连接生命周期
                )

                # 测试连接
                async with cls.pool.acquire() as conn:
                    await conn.execute('SELECT 1')

                # 创建必要的表
                await cls.create_table()

                logging.info("PostgreSQL 连接已建立")
                return
            except asyncpg.PostgresError as e:
                retry_count += 1
                if retry_count >= max_retries:
                    logging.error("PostgreSQL 连接失败，已重试 %d 次，退出", max_retries)
                    raise ConnectionError(f"无法连接到 PostgreSQL 数据库: {str(e)}") from e
                else:
                    wait_time = 2 ** retry_count  # 指数退避策略
                    logging.warning("PostgreSQL 连接失败，正在重试 %d/%d 次，等待 %d 秒: %s",
                                    retry_count, max_retries, wait_time, str(e))
                    await asyncio.sleep(wait_time)
            except Exception as e:
                logging.error("PostgreSQL 初始化失败: %s", str(e))
                raise

    @classmethod
    async def close(cls) -> None:
        """关闭数据库连接池，释放资源"""
        if cls.pool:
            await cls.pool.close()
            logging.info("PostgreSQL 连接池已关闭")

    @classmethod
    async def create_table(cls) -> None:
        """创建用户信息表（如果不存在）"""
        if not cls.pool:
            raise ValueError("数据库连接池尚未初始化")

        try:
            async with cls.pool.acquire() as conn:
                await conn.execute('''
                    CREATE TABLE IF NOT EXISTS userinfo (
                        wecom TEXT,
                        wecom_id TEXT,
                        name TEXT,
                        password TEXT,
                        department TEXT,
                        position TEXT,
                        mobile TEXT,
                        language TEXT,
                        email TEXT,
                        avatar_text TEXT
                    )
                ''')
                logging.debug("用户信息表创建成功或已存在")
        except Exception as e:
            logging.error("创建表失败: %s", str(e))
            raise

    @classmethod
    async def add_user(cls, data: Dict[str, Any]) -> Dict[str, bool]:
        """添加用户信息"""
        if not cls.pool:
            raise ValueError("数据库连接池尚未初始化")

        # 使用锁保证同一时间只有一个线程进行数据库操作
        async with cls.lock:
            wecom = data.get('wecom', 'None')
            wecom_id = data.get('wecom_id', 0)
            name = data.get('name', 'None')
            password = data.get('password')
            if password is None:
                password = hashlib.md5((str(name) + str(wecom_id)).encode()).hexdigest()
            else:
                password = hashlib.md5(password.encode()).hexdigest()
            department = data.get('department', 'None')
            position = data.get('position', 'B312')
            mobile = "None"
            email = data.get('email', f"{wecom_id}@bj35.com")
            language = data.get('language', 'zh')
            avatar_text = data.get('avatar', 'None')

            try:
                async with cls.pool.acquire() as conn:
                    await conn.execute('''
                        INSERT INTO userinfo (wecom, wecom_id, name, password, department, position, mobile, language, email, avatar_text)
                        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
                    ''', wecom, wecom_id, name, password, department, position, mobile, language, email, avatar_text)

                    logging.info("用户信息已添加: %s", name)
                    return {'success': True}
            except asyncpg.PostgresError as e:
                logging.error("添加用户失败: %s", str(e))
                return {'success': False}
            except Exception as e:
                logging.error("添加用户时发生未知错误: %s", str(e))
                return {'success': False}

    @classmethod
    async def verify_user_credentials(cls, username: str, password: str) -> Optional[tuple]:
        """直接验证用户凭据"""
        if not cls.pool:
            raise ValueError("数据库连接池尚未初始化")

        # 使用锁保证同一时间只有一个线程进行数据库操作
        async with cls.lock:
            try:
                async with cls.pool.acquire() as conn:
                    row = await conn.fetchrow("""
                        SELECT
                            CASE
                                WHEN wecom = $1 THEN 'wecom'
                                WHEN name = $1 THEN 'name'
                                WHEN email = $1 THEN 'email'
                                WHEN mobile = $1 THEN 'mobile'
                            END as kind,
                            password
                        FROM userinfo
                        WHERE wecom = $1 OR name = $1 OR email = $1 OR mobile = $1
                        LIMIT 1
                    """, username)

                    if row and row['kind'] and row['password'] == password:
                        return (username, row['kind'])
                    return None
            except Exception as e:
                logging.error("验证用户凭据失败: %s", str(e))
                raise

    @classmethod
    async def check_user_exists_by_wecom(cls, wecom_id: str) -> bool:
        """检查企业微信用户是否存在"""
        if not cls.pool:
            raise ValueError("数据库连接池尚未初始化")

        # 使用锁保证同一时间只有一个线程进行数据库操作
        async with cls.lock:
            try:
                async with cls.pool.acquire() as conn:
                    row = await conn.fetchrow("""
                        SELECT 1 FROM userinfo WHERE wecom_id = $1 LIMIT 1
                    """, int(wecom_id))

                    return bool(row)
            except Exception as e:
                logging.error("检查企业微信用户是否存在失败: %s", str(e))
                return False

    @classmethod
    async def get_password_by_username(cls, username: str, kind: str) -> Optional[str]:
        """根据用户名获取密码"""
        if not cls.pool:
            raise ValueError("数据库连接池尚未初始化")

        # 使用锁保证同一时间只有一个线程进行数据库操作
        async with cls.lock:
            allowed_columns = ['wecom', 'name', 'email', 'mobile']
            if kind not in allowed_columns:
                logging.error("无效的列名: %s", kind)
                raise ValueError(f"无效的列名: {kind}")

            try:
                async with cls.pool.acquire() as conn:
                    query = f"SELECT password FROM userinfo WHERE {kind} = $1"
                    password_sha256 = await conn.fetchval(query, username)
                    return password_sha256
            except Exception as e:
                logging.error("获取密码失败: %s", str(e))
                raise

    @classmethod
    async def get_userinfo_by_username(cls, username: str, kind: str) -> Optional[Dict[str, Any]]:
        """根据用户名获取用户信息"""
        if not cls.pool:
            raise ValueError("数据库连接池尚未初始化")

        # 使用锁保证同一时间只有一个线程进行数据库操作
        async with cls.lock:
            allowed_columns = ['wecom', 'name', 'email', 'mobile', 'wecom_id']
            if kind not in allowed_columns:
                logging.error("无效的列名: %s", kind)
                raise ValueError(f"无效的列名: {kind}")

            try:
                async with cls.pool.acquire() as conn:
                    query = f"SELECT * FROM userinfo WHERE {kind} = $1"
                    row = await conn.fetchrow(query, username)

                    if row:
                        # 将记录转换为字典
                        user_info_dict = dict(row)
                        logging.debug("已获取用户信息: %s", user_info_dict)
                        return user_info_dict
                    
                    logging.debug("未找到用户: %s", username)
                    return None
            except Exception as e:
                logging.error("获取用户信息失败: %s", str(e))
                raise

    @classmethod
    async def update_userinfo(cls, data: Dict[str, Any]) -> Dict[str, bool]:
        """更新用户信息"""
        if not cls.pool:
            raise ValueError("数据库连接池尚未初始化")

        # 使用锁保证同一时间只有一个线程进行数据库操作
        async with cls.lock:
            if 'name_old' not in data:
                raise ValueError("缺少必要的 'name_old' 字段")

            name = data['name_old']
            if len(data) < 2:
                raise ValueError("没有提供要更新的字段")

            # 获取第一个不是 'name_old' 的键作为要更新的字段
            update_kind = next((k for k in data.keys() if k != 'name_old'), None)
            if not update_kind:
                raise ValueError("没有提供要更新的字段")

            value = data[update_kind]

            # 验证更新的列名以防止SQL注入
            allowed_columns = ['wecom', 'wecom_id', 'name', 'password', 'department',
                               'position', 'mobile', 'language', 'email', 'avatar_text']
            if update_kind not in allowed_columns:
                logging.error("无效的列名: %s", update_kind)
                raise ValueError(f"无效的列名: {update_kind}")

            try:
                async with cls.pool.acquire() as conn:
                    query = f"UPDATE userinfo SET {update_kind} = $1 WHERE name = $2"
                    await conn.execute(query, value, name)
                    logging.info("已更新用户 信息: %s", {update_kind: value, 'name': name})
                    return {"success": True}
            except Exception as e:
                logging.error("更新用户信息失败: %s", str(e))
                raise
