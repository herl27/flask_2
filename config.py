# 配置文件
import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # 用于保护表单免受跨站请求伪造的KEY
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess str'
    # 因未存在BUG，不建议使用此特性，手动commit
    # SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    # 网站自动发出邮件标题的前缀
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    # 网站自动发出邮件的发件人
    FLASKY_MAIL_SENDER = 'Flasky管理员 <flasky@example.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 疑问：这个静态方法为什么会起作用？
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    # 网站自动发出邮件的发件服务器
    MAIL_SERVER = ''
    MAIL_PORT = 25
    MAL_USE_SSL = True
    # 邮件发送账户与密码，因涉及私密信息，放到环境变量里面，不要直接写在代码中
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    # 数据库位置
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URI') or \
        'sqlite:///' + os.path.join(basedir, db, date-dev.db)

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URI') or \
        'sqlite:///' + os.path.join(basedir, db, date-test.db)

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
        'sqlite:///' + os.path.join(basedir, db, date.db)

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}