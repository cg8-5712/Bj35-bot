"""
This file contains the code for registering the index route.
"""

def register_routes(app):
    """注册首页路由"""

    # 首页路由
    @app.route('/')
    def index():
        return """
        <html>
        <head>
            <title>BJ35-Bot API Server</title>
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 20px; }
                h1 { color: #333; border-bottom: 1px solid #eee; padding-bottom: 10px; }
                a { color: #0066cc; }
            </style>
        </head>
        <body>
            <h1>Welcome to BJ35-Bot API Server</h1>
            <p>This server provides APIs for controlling and monitoring robots.</p>
            <p>For more information, please visit
               <a href="https://github.com/cg8-5712/Bj35-bot/blob/main/Backend/readme.md">
               Readme.md</a>
            </p>
        </body>
        </html>
        """
