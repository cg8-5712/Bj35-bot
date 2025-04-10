from . import index, auth_routes, robot_routes, task_routes, user_routes, message_routes

def register_all_routes(app):
    """注册所有路由到应用实例"""
    index.register_routes(app)
    auth_routes.register_routes(app)
    robot_routes.register_routes(app)
    task_routes.register_routes(app)
    user_routes.register_routes(app)
    message_routes.register_routes(app)