import aiosqlite
import hashlib

"""
    数据库

    wecom: 老师工号
    wecom_id: 老师企微的user_id
    name: 老师姓名
    password: 老师密码
    department: 老师部门（可选）
    position: 老师职位（可选）
    mobile: 老师手机号
    language: 老师语言（默认Chinese）
    email: 老师邮箱（可选）
    avatar_text: 老师头像文字（可选）

"""

class SqliteData:

    @classmethod
    async def initialize(cls):
        cls.conn = await aiosqlite.connect('user-data.sqlite')
        cls.cursor = await cls.conn.cursor()
        await cls.create_table()
        await cls.conn.commit()

    @classmethod
    async def create_table(cls):
        await cls.cursor.execute('''CREATE TABLE IF NOT EXISTS userinfo (
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
            )''')
        await cls.conn.commit()

    @classmethod
    async def get_login_username_list(cls):
        await cls.cursor.execute("SELECT wecom, name, email, mobile FROM userinfo")
        rows = await cls.cursor.fetchall()
        username = {
            'wecom': [row[0] for row in rows],
            'name': [row[1] for row in rows],
            'email': [row[2] for row in rows],
            'mobile': [row[3] for row in rows],
        }
        return username

    @classmethod
    async def get_password_by_username(cls, username, kind):
        await cls.cursor.execute("SELECT password FROM userinfo WHERE " + kind + " = ?", (username,))
        password_sha256 = await cls.cursor.fetchone()
        return password_sha256[0] if password_sha256 else None

    @classmethod
    async def get_userinfo_by_username(cls, username, kind):
        await cls.cursor.execute("SELECT * FROM userinfo WHERE " + kind + " = ?", (username,))
        user_info = await cls.cursor.fetchone()
        print(user_info)
        return user_info if user_info else None