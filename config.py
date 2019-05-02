import os


basepath = os.path.dirname(__file__)


class CommonConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'rUNiZjNx$5$2s^U1'
    AUTH = True

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(CommonConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:passwd@localhost:3306/test?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REDIS_URL = "redis://:@localhost:6379/0"
    UPLOAD_FOLDER = os.path.join(basepath, 'static')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    STATIONS = {'1.起点站', '2.南书院站', '3.图书馆站', '4.九/十一号教学楼站', '5.八号教学楼站', '6.十号教学楼站', '7.十五号教学楼站'}
    DOMAIN = ''
    AUTH = False


class ProductConfig(CommonConfig):
    # SQLAlchemy 的设置
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:passwd@localhost:3306/test?charset=utf8'


config = {
    # 三种配置的选择
    'devConfig': DevelopmentConfig,
    'proConfig': ProductConfig,
    # 默认配置的设置
    'default': DevelopmentConfig
}
