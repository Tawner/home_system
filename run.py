from apps import create_app
from flask import request
from common.models.model import User
import os
app, manager = create_app(os.getenv('FLASK_CONFIG') or 'development')


@app.before_request
def identity_check():
    path = request.path
    if path.split('/')[-1].isdigit():
        path = '/'.join(path.split('/')[:-1]) + '/'

    # 白名单
    if path in app.config['WHITE_HOST']:
         return None

    # 开发板接口
    if path in app.config['HOME_SYSTEM_HOST']:
        linux_key = request.values.get('linux_key', '')
        if linux_key == app.config['LINUX_KEY']:
            return None
        else:
            return {"code": 201, "msg": "linux_key checkout failure"}

    # 登陆验证
    token = request.headers.get('Authorization', None)
    if token:
        user = User.check_token(token)
        if user: request.current_user = user
        return None
    else:
        return {"code": 201, "msg": "token校验失败"}


if __name__ == '__main__':
    manager.run()
