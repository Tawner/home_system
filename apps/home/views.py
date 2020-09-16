from common.models.model import *
from flask_restful import Resource, Api, marshal
from flask import Blueprint
from apps.home.param_parse import *
from apps.home.marshals import *

home_bp = Blueprint('home', __name__)
home_api = Api(home_bp)
linux_bp = Blueprint('linux', __name__)
linux_api = Api(linux_bp)


# 前端接口
class GetRoomDataView(Resource):

    def get(self):
        req_val = RoomDataParse()()
        if req_val['type']:
            home = Home.query.filter(Home.is_delete == 0).order_by(Home.id.desc()).limit(7).all()
            home.sort(key=lambda x: x.time)
        else:
            home = Home.query.filter(Home.is_delete == 0).order_by(Home.id.desc()).first()
        if home: return {"code": 200, "data": marshal(home, home_fields)}
        else: return {"code": 201, "msg": "没有数据"}


class DeviceDataView(Resource):

    def get(self):
        set_obj = Setting.query.filter(Setting.is_delete == 0).order_by(Setting.id.desc()).first()
        if set_obj: return {"code": 200, "data": marshal(set_obj, setting_fields)}
        else: return {"code": 201, "msg": "没有数据"}

    def put(self):
        req_val = ModifySettingParse()()
        Setting.query.filter(Setting.is_delete == 0).update(req_val)
        db.session.commit()
        return {"code": 200, "msg": "修改成功"}


home_api.add_resource(GetRoomDataView, '')
home_api.add_resource(DeviceDataView, '/setting')


# 开发板接口
class LinuxRoomDataView(Resource):

    def post(self):
        req_val = AddHomeDataParse()()
        home = Home.query.filter(Home.is_delete == 0).order_by(Home.id.desc()).first()
        home_data = marshal(home, home_fields)
        home_data.update(req_val)
        home_obj = Home(**home_data)
        db.session.add(home_obj)
        db.session.commit()
        return {"code": 200, "msg": "add success"}


class LinuxDeviceDataView(Resource):

    def get(self):
        set_obj = Setting.query.filter(Setting.is_delete == 0).order_by(Setting.id.desc()).first()
        if set_obj: return {"code": 200, "data": marshal(set_obj, setting_fields)}
        else: return {"code": 201, "msg": "not data"}

    def post(self):
        req_val = LinuxModifySettingParse()()
        Setting.query.filter(Setting.is_delete == 0).update(req_val)
        db.session.commit()
        return {"code": 200, "msg": "update success"}


linux_api.add_resource(LinuxRoomDataView, '/home')
linux_api.add_resource(LinuxDeviceDataView, '/device')
