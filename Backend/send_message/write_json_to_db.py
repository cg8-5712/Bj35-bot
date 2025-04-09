import sys
import os
import json
import asyncio

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from handler.PostgreSQLConnector import PostgreSQLConnector
import handler.config

async def main():
    try:
        await PostgreSQLConnector.initialize()
    except Exception as e:
        print(f"数据库初始化失败，应用将退出: {e}")
        exit(1)

    with open('users_dev.json', 'r', encoding='utf-8') as f:
        data = json.loads(f.read())

    for user in data:
        user_data = {}

        user_data['wecom'] = user.get('alias', "None")
        user_data['wecom_id'] = int(user.get('userid', 0000))
        user_data['name'] = user.get('name', 'None')
        user_data['department'] = user.get('department', 'None')

        department = user.get('department', 'None')
        if isinstance(department, list):
            user_data['department'] = ','.join(map(str, user.get('department', [])))
        else:
            user_data['department'] = department

        user_data['position'] = user.get('position', 'None')
        user_data['mobile'] = user.get('telephone', 'None')
        user_data['email'] = user.get('email', 'None')

        try:
            await PostgreSQLConnector.add_user(user_data)
            print(user_data)
        except Exception as e:
            print(f"添加用户时发生未知错误: {e}")

asyncio.run(main())
