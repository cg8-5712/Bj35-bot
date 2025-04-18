"""
Bj35 Bot v2
Refactor by: AptS:1547
Date: 2025-04-19
Description: 这是在 v1 基础上重构的版本，主要改进了代码结构和可读性。
使用 GPLv3 许可证。
Copyright (C) 2025 AptS:1547
"""

import sys
import logging
from pathlib import Path

from dotenv import load_dotenv

from quart import Quart
from quart_cors import cors
from quart_jwt_extended import JWTManager

from settings import settings
from utils import PostgreSQLConnector
from utils import configure_jwt_handlers
from services import TokenManager

from routes import register_all_routes

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def create_app():
    """应用工厂函数"""
    quart_app = Quart(__name__)

    # 配置CORS和JWT
    quart_app = cors(quart_app, allow_origin="*")
    quart_app.config["JWT_SECRET_KEY"] = settings.AUTH_JWT_SECRET_KEY
    jwt = JWTManager(quart_app)

    # 配置JWT错误处理器
    configure_jwt_handlers(jwt)

    # 注册所有路由
    register_all_routes(quart_app)

    return quart_app

# 创建应用实例
app = create_app()

async def init_db():
    try:
        await PostgreSQLConnector.initialize()
    except Exception as e:
        if settings.ENV == 'development':
            logging.error("数据库初始化失败: %s", e)
            return

        logging.critical("数据库初始化失败，应用将退出: %s", e)
        exit(1)

@app.before_serving
async def before_serving():
    env = settings.ENV

    # 使用 pathlib 替代 os.path
    base_path = Path.cwd()  # 获取当前工作目录
    env_specific_file = base_path / f".env.{env}"
    default_env_file = base_path / ".env"

    env_file = env_specific_file if env_specific_file.exists() else default_env_file

    load_dotenv(env_file)
    logging.info("加载环境变量文件: %s", env_file)

    await init_db()
    if await TokenManager.get_valid_token():
        TokenManager.log_token_expiry()
    else:
        logging.error("获取有效的token失败，应用将退出")
        sys.exit(1)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
