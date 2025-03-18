import sqlite3

class SqliteData:

    @classmethod
    def initialize(cls):
        cls.conn = sqlite3.connect('user-data.sqlite')
        cls.cursor = cls.conn.cursor()
        cls.create_table()
        cls.conn.commit()

    @classmethod
    def create_table(cls):
        cls.cursor.execute('''CREATE TABLE IF NOT EXISTS userinfo (
                wecom_id INTEGER,
                password TEXT,
                name TEXT,
                department TEXT,
                position TEXT,
                mobile TEXT,
                email TEXT,
                avatar_url TEXT
            )''')
        cls.conn.commit()