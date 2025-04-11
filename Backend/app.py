# -*- coding: utf-8 -*-

import logging
import datetime
from quart import Quart
from quart_cors import cors
from quart_jwt_extended import JWTManager

from utils import Config, PostgreSQLConnector
from utils import configure_jwt_handlers, update_access_token

from routes import register_all_routes

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def create_app():
    """应用工厂函数"""
    app = Quart(__name__)

    # 配置CORS和JWT
    app = cors(app, allow_origin="*")
    app.config["JWT_SECRET_KEY"] = Config.jwt_secret_key()
    jwt = JWTManager(app)

    # 配置JWT错误处理器
    configure_jwt_handlers(jwt)

    # 注册所有路由
    register_all_routes(app)

    return app

async def check_token():
    """
    检查access token是否在当天过期，如果是则更新。
    """
    try:
        expiration_ts = float(Config.expire_time())
        expire_date = datetime.datetime.fromtimestamp(expiration_ts)
        today = datetime.datetime.now().date()
        if expire_date.date() == today:
            logging.info("Access token将在今天过期，开始生成新的access token。")
            result = await update_access_token()
            if result:
                logging.info("新的access token生成成功。")
            else:
                logging.error("生成新的access token失败：%s", result)
    except Exception as e:
        logging.error("检查或更新access token时出错：%s", str(e))

def log_token_expiry():
    """启动时获取expiration并记录距离过期的天数"""
    try:
        expiration_ts = float(Config.expire_time())
        current_ts = datetime.datetime.now().timestamp()
        days_remaining = (expiration_ts - current_ts) / (60 * 60 * 24)
        logging.info("Access token将在 %i 天后过期。", days_remaining)
    except Exception as e:
        logging.error("获取token过期时间失败：%s", str(e))

# 创建应用实例
app = create_app()

async def init_db():
    try:
        await PostgreSQLConnector.initialize()
    except Exception as e:
        if Config.get_env() == 'development':
            logging.error("数据库初始化失败: %s", e)
            return

        logging.critical("数据库初始化失败，应用将退出: %s", e)
        exit(1)

@app.before_serving
async def before_serving():
    await init_db()
    log_token_expiry()
    await check_token()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
