import os

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class BaseConfig(object):
    SECRET_KEY = os.getenv('SECRET_KEY', 'fgz_home_system')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_RECYCLE = 200
    UPLOAD_FOLDER = os.path.join(basedir, 'uploads')
    STATIC_FOLDER = UPLOAD_FOLDER
    ALLOWED_IMAGE = ['png', 'jpg', 'jpeg']
    ALLOWED_FILE = ['xlsx']
    ALLOWED_EXTENSIONS = ALLOWED_IMAGE + ALLOWED_FILE
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB

    # 无需登陆接口
    WHITE_HOST = ["/api/user/login"]

    # 开发板接口
    HOME_SYSTEM_HOST = ["/api/linux/home", "/api/linux/device"]

    # 开发板秘钥
    LINUX_KEY = "home_system_fgz"

    # redis数据库
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    REDIS_DB = 8  # 数据库名


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:xxxx@127.0.0.1:3306/home_system?charset=utf8'
    WEB_HOST_NAME = 'http://127.0.0.1:5000/'


class TestingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:xxxx@127.0.0.1:3306/home_system?charset=utf8'
    WEB_HOST_NAME = 'http://127.0.0.1:5000/'


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:xxxx@127.0.0.1:3306/home_system?charset=utf8'
    WEB_HOST_NAME = 'http://127.0.0.1:5000/'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}