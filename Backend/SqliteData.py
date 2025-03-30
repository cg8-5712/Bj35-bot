import aiosqlite


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
        if user_info:
            # 获取列名
            columns = [column[0] for column in cls.cursor.description]
            # 将列名与查询结果组合成字典
            user_info_dict = dict(zip(columns, user_info))
            print(user_info_dict)
            return user_info_dict
        else:
            return None

    @classmethod
    async def update_userinfo(cls, username, kind, value):
        await cls.cursor.execute("UPDATE userinfo SET " + kind + " = ? WHERE wecom = ?", (value, username))
        await cls.conn.commit()
