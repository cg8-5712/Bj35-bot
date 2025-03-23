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
                wecom INTEGER,
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
        cls.conn.commit()