from common.models.model import *
from flask_restful import Resource, Api, marshal
from flask import Blueprint
from apps.user.param_parse import *
from apps.user.marshals import *
from flask import request

user_bp = Blueprint('user', __name__)
user_api = Api(user_bp)


class UserInfoView(Resource):

    def get(self):
        return {"code": 200, "data": marshal(request.current_user, user_fields)}

    def put(self):
        req_val = UpdateUserParse()()
        if req_val['password'] != req_val['password_2']: return {"code": 202, "msg": "两次密码不一致"}
        req_val.pop('password_2')
        res = request.current_user.update(**req_val)
        if res['status'] == 'failure': return {"code": 202, "msg": res.get('msg', '')}
        else: return {"code": 200, "msg": "修改成功"}

    def post(self):
        req_val = AddUserParse()()
        if req_val['password'] != req_val['password_2']: return {"code": 202, "msg": "两次密码不一致"}
        req_val.pop('password_2')
        User.add(**req_val)
        return {"code": 200, "msg": "添加成功"}


class UserLoginView(Resource):

    def post(self):
        req_val = UserLoginParse()()
        res = User.check_password(**req_val)
        if res['status'] == 'failure': return {"code": 202, "msg": res['msg']}
        return {"code": 200, "token": res['user'].create_token()}


user_api.add_resource(UserInfoView, '/info')
user_api.add_resource(UserLoginView, '/login')

