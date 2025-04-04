import asyncio
import asyncpg
import logging
from typing import Dict, List, Optional, Any, Union

class PostgreSQLConnector:
    """PostgreSQL 数据库连接管理类，提供数据库操作的各种方法。"""
    pool: Optional[asyncpg.Pool] = None
    
    @classmethod
    async def initialize(cls, config=None) -> None:
        if cls.pool:
            logging.info("数据库连接池已存在，跳过初始化")
            return
        
        # Config模块获取配置，若未传入
        if config is None:
            try:
                from handler.config import Config
                config = Config.database_config()
            except (ImportError, AttributeError):
                logging.warning("无法从Config获取数据库配置，使用默认配置")
                config = {
                    'host': 'localhost', 
                    'port': 5432,
                    'database': 'userdata', 
                    'user': 'postgres',
                    'password': 'password', 
                    'min_size': 5, 
                    'max_size': 10
                }

        db_host = config.get('host', 'localhost')
        db_port = config.get('port', 5432)
        db_name = config.get('database', 'userdata')
        db_user = config.get('user', 'postgres')
        db_pass = config.get('password', 'password')
        min_size = config.get('min_size', 5)
        max_size = config.get('max_size', 10)

        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                # 创建连接池
                cls.pool = await asyncpg.create_pool(
                    host=db_host,
                    port=db_port,
                    database=db_name,
                    user=db_user,
                    password=db_pass,
                    min_size=min_size,
                    max_size=max_size
                )
                
                # 测试连接
                async with cls.pool.acquire() as conn:
                    await conn.execute('SELECT 1')
                
                # 创建必要的表
                await cls.create_table()
                
                logging.info(f"PostgreSQL 连接已建立 (主机: {db_host}, 数据库: {db_name})")
                return
            except asyncpg.PostgresError as e:
                retry_count += 1
                if retry_count >= max_retries:
                    logging.error(f"PostgreSQL 连接失败，已重试 {max_retries} 次: {e}")
                    raise ConnectionError(f"无法连接到 PostgreSQL 数据库: {str(e)}")
                else:
                    wait_time = 2 ** retry_count  # 指数退避策略
                    logging.warning(f"PostgreSQL 连接失败，{wait_time} 秒后重试 ({retry_count}/{max_retries}): {e}")
                    await asyncio.sleep(wait_time)
            except Exception as e:
                logging.error(f"PostgreSQL 初始化失败: {e}")
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
                        wecom_id INTEGER,
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
            logging.error(f"创建表失败: {e}")
            raise
    
    @classmethod
    async def verify_user_credentials(cls, username: str, password: str) -> Optional[tuple]:
        """
        直接验证用户凭据
        
        Args:
            username: 用户名/邮箱/手机号等标识符
            password: 用户提供的密码
            
        Returns:
            如果验证成功，返回 (username, kind) 元组；验证失败返回 None
        """
        if not cls.pool:
            raise ValueError("数据库连接池尚未初始化")
            
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
            logging.error(f"验证用户凭据失败: {e}")
            raise
    
    @classmethod
    async def get_password_by_username(cls, username: str, kind: str) -> Optional[str]:
        """
        根据用户名获取密码
        
        Args:
            username: 用户标识符(用户名/邮箱/手机等)
            kind: 标识符类型，如 'wecom', 'name', 'email', 'mobile'
            
        Returns:
            用户密码的哈希值，如果用户不存在则返回 None
            
        Raises:
            ValueError: 如果提供了无效的列名
        """
        if not cls.pool:
            raise ValueError("数据库连接池尚未初始化")
            
        # 验证列名以防止SQL注入
        allowed_columns = ['wecom', 'name', 'email', 'mobile']
        if kind not in allowed_columns:
            logging.error(f"无效的列名: {kind}")
            raise ValueError(f"无效的列名: {kind}")
        
        try:
            async with cls.pool.acquire() as conn:
                query = f"SELECT password FROM userinfo WHERE {kind} = $1"
                password_sha256 = await conn.fetchval(query, username)
                return password_sha256
        except Exception as e:
            logging.error(f"获取密码失败: {e}")
            raise
    
    @classmethod
    async def get_userinfo_by_username(cls, username: str, kind: str) -> Optional[Dict[str, Any]]:
        """
        根据用户标识符获取用户信息
        
        Args:
            username: 用户标识符
            kind: 标识符类型，如 'wecom', 'name', 'email', 'mobile', 'wecom_id'
            
        Returns:
            用户信息字典，不存在则返回 None
            
        Raises:
            ValueError: 如果提供了无效的列名
        """
        if not cls.pool:
            raise ValueError("数据库连接池尚未初始化")
            
        # 验证列名以防止SQL注入
        allowed_columns = ['wecom', 'name', 'email', 'mobile', 'wecom_id']
        if kind not in allowed_columns:
            logging.error(f"无效的列名: {kind}")
            raise ValueError(f"无效的列名: {kind}")
        
        try:
            async with cls.pool.acquire() as conn:
                query = f"SELECT * FROM userinfo WHERE {kind} = $1"
                row = await conn.fetchrow(query, username)
                
                if row:
                    # 将记录转换为字典
                    user_info_dict = dict(row)
                    logging.debug(f"已获取用户信息: {user_info_dict.get('name', 'unknown')}")
                    return user_info_dict
                else:
                    logging.debug(f"未找到用户: {username} (通过 {kind})")
                    return None
        except Exception as e:
            logging.error(f"获取用户信息失败: {e}")
            raise
    
    @classmethod
    async def update_userinfo(cls, data: Dict[str, Any]) -> Dict[str, bool]:
        """
        更新用户信息
        
        Args:
            data: 包含更新信息的字典，必须包含 'name_old' 键以及需要更新的字段
            
        Returns:
            包含操作结果的字典
            
        Raises:
            ValueError: 如果提供了无效的列名或数据格式不正确
        """
        if not cls.pool:
            raise ValueError("数据库连接池尚未初始化")
            
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
            logging.error(f"无效的列名: {update_kind}")
            raise ValueError(f"无效的列名: {update_kind}")
            
        try:
            async with cls.pool.acquire() as conn:
                query = f"UPDATE userinfo SET {update_kind} = $1 WHERE name = $2"
                await conn.execute(query, value, name)
                logging.info(f"已更新用户 {name} 的 {update_kind} 字段")
                return {"success": True}
        except Exception as e:
            logging.error(f"更新用户信息失败: {e}")
            raise
