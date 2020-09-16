from flask_restful import reqparse
from common.libs import inputs


class BaseParse():
    def __init__(self):
        self.parse = reqparse.RequestParser()


class AddUserParse(BaseParse):
    def __call__(self):
        self.parse.add_argument('username', type=inputs.str_range(6, 16), required=True)
        self.parse.add_argument('password', type=inputs.str_range(6, 32), required=True)
        self.parse.add_argument('password_2', type=inputs.str_range(6, 32))
        self.parse.add_argument('nickname', type=inputs.str_range(3, 32), default='admin')
        self.parse.add_argument('email', type=inputs.str_range(3, 128), default=None)
        self.parse.add_argument('phone', type=inputs.str_range(11, 11), default=None)
        self.parse.add_argument('image_id', type=inputs.image_parse, default=None)
        return self.parse.parse_args()


class UpdateUserParse(BaseParse):
    def __call__(self):
        self.parse.add_argument('password', type=inputs.str_range(6, 32))
        self.parse.add_argument('password_2', type=inputs.str_range(6, 32))
        self.parse.add_argument('nickname', type=inputs.str_range(3, 32))
        self.parse.add_argument('email', type=inputs.str_range(3, 128))
        self.parse.add_argument('phone', type=inputs.str_range(11, 11))
        self.parse.add_argument('image_id', type=inputs.image_parse)
        return self.parse.parse_args()


class UserLoginParse(BaseParse):
    def __call__(self):
        self.parse.add_argument('username', type=inputs.str_range(6, 16))
        self.parse.add_argument('password', type=inputs.str_range(6, 32))
        return self.parse.parse_args()


