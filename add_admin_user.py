import asyncio
import hashlib
import aiosqlite

async def add_admin_user():
    # 连接到数据库
    conn = await aiosqlite.connect('user-data.sqlite')
    cursor = await conn.cursor()
    
    # 对密码进行SHA256哈希
    password_hash = hashlib.sha256('password'.encode()).hexdigest()
    
    # 插入admin用户
    await cursor.execute(
        "INSERT INTO userinfo (name, password) VALUES (?, ?)",
        ('admin', password_hash)
    )
    
    # 提交更改并关闭连接
    await conn.commit()
    await conn.close()
    print("成功添加admin用户")

# 运行异步函数
asyncio.run(add_admin_user())