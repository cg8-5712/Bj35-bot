import aiosqlite
import hashlib

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

