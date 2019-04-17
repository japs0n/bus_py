import os


class CommonConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'rUNiZjNx$5$2s^U1'
    AUTH = True
    # SMS服务相关
    SMS_APPKEY = ''
    SMS_APPID = ''
    SMS_SIGN = ''
    SMS_TEMPLATE = ''

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(CommonConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost:3306/equipments?charset=utf8'
    AUTH = False


class ProductConfig(CommonConfig):
    # SQLAlchemy 的设置
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost:3306/equipments?charset=utf8'


config = {
    # 三种配置的选择
    'devConfig': DevelopmentConfig,
    'proConfig': ProductConfig,
    # 默认配置的设置
    'default': DevelopmentConfig
}