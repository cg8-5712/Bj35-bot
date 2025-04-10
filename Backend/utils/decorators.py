from functools import wraps
from quart import jsonify
import logging

from handler.accessToken import update_access_token

def error_handler(func):
    """异常处理装饰器"""

    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            response = await func(*args, **kwargs)
            if type(response) is dict:
                response_json = response.get_json()
                response_json = await func(*args, **kwargs)
                if response_json.get('code') == 11013:
                    logging.error(f"Authentication failed in {func.__name__}: {response_json}")
                    await update_access_token()
                    return jsonify(response_json), response.status_code
            return response
        except Exception as e:
            logging.error(f"Error in {func.__name__}: {str(e)}")
            return jsonify({'code': 1, 'message': str(e), 'data': []}), 500

    return wrapper