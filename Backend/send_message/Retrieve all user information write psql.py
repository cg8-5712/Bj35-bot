import requests
import pandas as pd
from time import time
import psycopg2  # 新增数据库驱动
from psycopg2 import sql
from psycopg2.extras import execute_batch  # 用于批量插入

CORP_ID = "ww8e4628d565c6588f"
CORP_SECRET = "f03d8WfJfKpgX3NG84pXMaN7a6G1xOY2QummZNZh_Xg"

class WeComAPI:
    def __init__(self, corpid, corpsecret, db_config=None):
        self.corpid = corpid
        self.corpsecret = corpsecret
        self.token_expire = 0
        self.access_token = ""
        self.db_config = db_config or {  # 新增数据库配置
            "host": "localhost",
            "port": "5432",
            "dbname": "your_db",
            "user": "your_user",
            "password": "your_password"
        }

    # ... 保持原有 _get_access_token 和 get_all_users_basic 方法不变 ...

    def _create_users_table(self, conn):
        """创建用户信息表（如果不存在）"""
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS wecom_users (
            userid VARCHAR(64) PRIMARY KEY,
            name VARCHAR(128) NOT NULL,
            department TEXT,
            position VARCHAR(128),
            mobile VARCHAR(32),
            email VARCHAR(128),
            status INT
        );
        """
        try:
            with conn.cursor() as cursor:
                cursor.execute(create_table_sql)
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"创建表失败: {e}")

    def _write_to_database(self, users):
        """将用户数据写入数据库"""
        if not self.db_config:
            print("未配置数据库信息")
            return False
        try:
            conn = psycopg2.connect(**self.db_config)
            self._create_users_table(conn)

            insert_sql = sql.SQL("""
                INSERT INTO wecom_users 
                (userid, name, department, position, mobile, email, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (userid) DO UPDATE SET
                    name = EXCLUDED.name,
                    department = EXCLUDED.department,
                    position = EXCLUDED.position,
                    mobile = EXCLUDED.mobile,
                    email = EXCLUDED.email,
                    status = EXCLUDED.status
            """)
            # 准备批量数据
            batch_data = []
            for user in users:
                batch_data.append((
                    user.get("userid"),
                    user.get("name"),
                    ",".join(map(str, user.get("department", []))),
                    user.get("position"),
                    user.get("mobile"),
                    user.get("email"),
                    user.get("status", 1)
                ))
            with conn.cursor() as cursor:
                execute_batch(cursor, insert_sql, batch_data)
                conn.commit()
                print(f"成功写入 {len(batch_data)} 条数据到数据库")
                return True
        except Exception as e:
            print(f"数据库操作失败: {e}")
            conn.rollback()
            return False
        finally:
            if 'conn' in locals():
                conn.close()

    def export_all(self, excel_filename="user_list.xlsx"):
        """同时导出到Excel和数据库"""
        users = self.get_all_users_basic()
        if not users:
            print("没有获取到用户数据")
            return False

        # 导出到Excel
        excel_result = self._export_to_excel(users, excel_filename)

        # 导出到数据库
        db_result = self._write_to_database(users)

        return excel_result and db_result

    def _export_to_excel(self, users, filename):
        """重构后的Excel导出方法"""
        data = [{
            "姓名": u.get("name", ""),
            "UserID": u.get("userid", ""),
            "部门": ",".join(map(str, u.get("department", []))),
            "职位": u.get("position", "")
        } for u in users]

        try:
            df = pd.DataFrame(data)
            df.to_excel(filename, index=False, engine="openpyxl")
            print(f"成功导出 {len(df)} 条数据到 {filename}")
            return True
        except Exception as e:
            print(f"导出Excel失败: {str(e)}")
            return False

# 修改后的使用示例
if __name__ == "__main__":
    # 企业微信配置
    # 数据库配置（按实际情况修改）
    DB_CONFIG = {
        "host": "192.168.101.138",
        "port": "54321",
        "dbname": "wecom",
        "user": "bj35bot",
        "password": "z84bkuf3RXvkjE7f"
    }

    wecom = WeComAPI(CORP_ID, CORP_SECRET, DB_CONFIG)

    # 同时导出到Excel和数据库
    if wecom.export_all("wecom_users.xlsx"):
        print("导出成功！")
    else:
        print("导出失败")