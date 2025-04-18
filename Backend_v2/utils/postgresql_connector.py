"""
Bj35 Bot v2
Refactor by: AptS:1547
Date: 2025-04-19
Description: 这是在 v1 基础上重构的版本，主要改进了代码结构和可读性。
使用 GPLv3 许可证。
Copyright (C) 2025 AptS:1547

本文件定义了PostgreSQLConnector类，用于管理PostgreSQL数据库连接和操作。
"""

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
    async def execute(cls, query: str, *args) -> None:
        """执行不返回结果的SQL语句"""
        if not cls.pool:
            raise ValueError("数据库连接池尚未初始化")

        async with cls.lock:
            try:
                async with cls.pool.acquire() as conn:
                    await conn.execute(query, *args)
            except Exception as e:
                logging.error("SQL执行失败: %s", str(e))
                raise

    @classmethod
    async def fetch_one(cls, query: str, *args) -> Optional[Dict[str, Any]]:
        """执行查询并返回一条记录"""
        if not cls.pool:
            raise ValueError("数据库连接池尚未初始化")

        async with cls.lock:
            try:
                async with cls.pool.acquire() as conn:
                    row = await conn.fetchrow(query, *args)
                    return dict(row) if row else None
            except Exception as e:
                logging.error("SQL查询失败: %s", str(e))
                raise

    @classmethod
    async def fetch_all(cls, query: str, *args) -> list:
        """执行查询并返回所有记录"""
        if not cls.pool:
            raise ValueError("数据库连接池尚未初始化")

        async with cls.lock:
            try:
                async with cls.pool.acquire() as conn:
                    rows = await conn.fetch(query, *args)
                    return [dict(row) for row in rows]
            except Exception as e:
                logging.error("SQL查询失败: %s", str(e))
                raise

    @classmethod
    async def fetch_val(cls, query: str, *args) -> Any:
        """执行查询并返回单个值"""
        if not cls.pool:
            raise ValueError("数据库连接池尚未初始化")
        
        async with cls.lock:
            try:
                async with cls.pool.acquire() as conn:
                    return await conn.fetchval(query, *args)
            except Exception as e:
                logging.error("SQL查询失败: %s", str(e))
                raise
