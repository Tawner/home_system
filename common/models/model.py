from common.models.base import Base, db
from common.libs.utility import *
from flask import current_app
import os


class Upload(Base):
    __tablename__ = 'upload'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    filename = db.Column(db.String(252), comment='文件名')
    file_md5 = db.Column(db.String(128), comment='文件md5')
    file_type = db.Column(db.SmallInteger, default=0, comment='文件类型')  # 0 图片 1 文件
    file_size = db.Column(db.Integer, default=0, comment='文件大小')
    path = db.Column(db.String(256), comment='文件路径')

    @property
    def url(self):
        path = 'file/' if self.file_type else 'image/'
        url = current_app.config['WEB_HOST_NAME'] + 'api/uploads/' + path + self.filename
        return url

    @classmethod
    def save_file(cls, file):
        if not file: return {'status': "failure", "msg": "没有上传文件"}

        filename, file_type = os.path.splitext(file.filename)
        if file_type[1:] in current_app.config['ALLOWED_IMAGE']: upload_type = 0
        elif file_type[1:] in current_app.config['ALLOWED_file']: upload_type = 1
        else: return {"status": "failure", "msg": "不允许上传的文件类型"}

        md5_code = md5(file.read())
        upload_file = Upload.query.filter(Upload.file_md5 == md5_code).first()
        if upload_file:
            return {"status": "success", "url": upload_file.url, 'id': upload_file.id}
        else:
            r_path = current_app.config['UPLOAD_FOLDER'] + 'file/' if upload_file else 'image/' + md5_code + file_type,
            inset_data = {
                "filename": md5_code + file_type,
                "file_md5": md5_code,
                "file_type": upload_type,
                "file_size": file.content_length,
                "path": r_path
            }
            upload_file = Upload(**inset_data)
            file.seek(0)
            file.save(r_path)
            db.session.add(upload_file)
            db.session.commit()
            return {"status": "success", "url": upload_file.url, 'id': upload_file.id}


class User(Base):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(16), nullable=False, comment='用户名')
    password = db.Column(db.String(32), nullable=False, comment='密码')
    encryption = db.Column(db.String(6), nullable=False, comment='密文')
    nickname = db.Column(db.String(32), comment='昵称')
    email = db.Column(db.String(128), comment='邮箱')
    phone = db.Column(db.String(11), comment='手机号码')

    # 外键、关联
    image_id = db.Column(db.Integer, db.ForeignKey('upload.id'))
    headimg = db.relationship("Upload", foreign_keys=[image_id])

    @staticmethod
    def check_password(username, password):
        user = User.query.filter(User.username == username).first()
        if not user: return {"status": "failure", "msg": "用户名不存在"}
        if md5(md5(password) + user.encryption) == user.password:
            return {"status": "success", "user": user}
        else:
            return {"status": "failure", "msg": "用户名或者密码错误"}

    @property
    def image(self):
        return self.headimg.url

    @classmethod
    def add(cls, username, password, nickname=None, email=None, phone=None, image_id=None):
        exist = User.query.filter(User.username == username).first()
        if exist: return {"status": "failure", "msg": "用户名已存在"}
        encryption = random_str(6)
        user = User(
            username=username,
            password=md5(md5(password) + encryption),
            encryption=encryption,
            nickname=nickname,
            email=email,
            phone=phone,
            image_id=image_id
        )
        db.session.add(user)
        db.session.commit()
        return {"status": "success", "user": user}

    def update(self, password=None, nickname=None, email=None, phone=None, image_id=None):
        if password: self.password = md5(md5(password) + self.encryption)
        if nickname: self.nickname = nickname
        if email: self.email = email
        if phone: self.phone = phone
        if image_id: self.image_id = image_id
        db.session.commit()
        return {"status": "success", "user": self}

    def create_token(self):
        return encrypt({"id": self.id})

    @classmethod
    def check_token(cls, token):
        token_data = decrypt(token)
        if not token_data: return None
        user = User.query.filter(User.id == token_data['id'], User.is_delete == 0).first()
        return user


class Home(Base):
    __tablename__ = 'home'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    time = db.Column(db.DateTime, nullable=False, comment='时间')
    temperature = db.Column(db.Float, default=0.0, comment='温度')
    humidity = db.Column(db.Float, default=0.0, comment='湿度')
    smoke = db.Column(db.Float, default=0.0, comment='烟雾浓度')
    light = db.Column(db.Float, default=0.0, comment='光照强度')
    pressure = db.Column(db.Float, default=0.0, comment='大气压强')
    altitude = db.Column(db.Float, default=0.0, comment='海拔')


class Setting(Base):
    __tablename__ = 'setting'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    temperature_max = db.Column(db.Float, default=0.0, comment='温度报警值')
    smoke_max = db.Column(db.Float, default=0.0, comment='烟雾报警值')
    humidity_max = db.Column(db.Float, default=0.0, comment='湿度报警值')
    air_switch = db.Column(db.SmallInteger, default=0, comment='空调开关')
    air_temperature = db.Column(db.Integer, default=26, comment='空调温度')
    air_model = db.Column(db.SmallInteger, default=0, comment='空调模式，0制冷，1制热，2通风')
    air_wind = db.Column(db.SmallInteger, default=0, comment="空调风速，0自动，1弱，2中，3强")
    air_wind_model = db.Column(db.SmallInteger, default=0, comment='0停止，1上下扫风，2左右扫风')
    lamp_model = db.Column(db.SmallInteger, default=0, comment='灯光模式，0关，1弱，2中，3强')
    curtains_switch = db.Column(db.SmallInteger, default=0, comment='窗帘开关')
    television_switch = db.Column(db.SmallInteger, default=0, comment='电视开关')
    television_chanel = db.Column(db.SmallInteger, default=0, comment='电视频道')
    music_switch = db.Column(db.SmallInteger, default=0, comment='音乐开关')



