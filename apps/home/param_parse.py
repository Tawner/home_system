from flask_restful import reqparse
from common.libs import inputs


class BaseParse():
    def __init__(self):
        self.parse = reqparse.RequestParser()


class RoomDataParse(BaseParse):
    def __call__(self):
        self.parse.add_argument('type', type=int, choices=(0, 1), default=0)
        return self.parse.parse_args()


class ModifySettingParse(BaseParse):
    def __call__(self):
        self.parse.add_argument('temperature_max', type=float)
        self.parse.add_argument('smoke_max', type=float)
        self.parse.add_argument('humidity_max', type=float)
        self.parse.add_argument('air_switch', type=int, choices=(0, 1))
        self.parse.add_argument('air_temperature', type=int)
        self.parse.add_argument('air_model', type=int, choices=(0, 1, 2))
        self.parse.add_argument('air_wind', type=int, choices=(0, 1, 2, 3))
        self.parse.add_argument('air_wind_model', type=int, choices=(0, 1, 2))
        self.parse.add_argument('lamp_model', type=int, choices=(0, 1, 2, 3))
        self.parse.add_argument('curtains_switch', type=int, choices=(0, 1))
        self.parse.add_argument('television_switch', type=int, choices=(0, 1))
        self.parse.add_argument('music_switch', type=int, choices=(0, 1))
        self.parse.add_argument('television_chanel', type=int)
        return self.parse.parse_args()


class AddHomeDataParse(BaseParse):
    def __call__(self):
        self.parse.add_argument('time', type=inputs.date_time(time_format="%Y-%m-%d %H:%M"), required=True)
        self.parse.add_argument('temperature', type=float)
        self.parse.add_argument('humidity', type=float)
        self.parse.add_argument('smoke', type=float)
        self.parse.add_argument('light', type=float)
        self.parse.add_argument('pressure', type=float)
        self.parse.add_argument('altitude', type=float)
        return self.parse.parse_args()


class LinuxModifySettingParse(ModifySettingParse):
    pass



