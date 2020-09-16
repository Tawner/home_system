from common.libs import fields

home_fields = {
    "time": fields.Datetime(dt_format='%Y-%m-%d %H:%M'),
    "temperature": fields.Float,
    "humidity": fields.Float,
    "smoke": fields.Float,
    "light": fields.Float,
    "pressure": fields.Float,
    "altitude": fields.Float
}

setting_fields = {
    "temperature_max": fields.Float,
    "smoke_max": fields.Float,
    "humidity_max": fields.Float,
    "air_switch": fields.Integer,
    "air_temperature": fields.Integer,
    "air_model": fields.Integer,
    "air_wind": fields.Integer,
    "air_wind_model": fields.Integer,
    "lamp_model": fields.Integer,
    "curtains_switch": fields.Integer,
    "television_switch": fields.Integer,
    "television_chanel": fields.Integer,
    "music_switch": fields.Integer,
}