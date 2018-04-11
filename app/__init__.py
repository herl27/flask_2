# 工厂函数
# 为了可以动态修改程序的配置
# 延迟创建程序实例，把创建过程移到可显式调用的工厂函数中
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config

# 创建扩展实例,放在这里为了全局使用
bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
login_manager.login_message = '请登陆'

def create_app(config_name):
    app = Flask(__name__)
    # app的配置利用app.config对象提供的from_object()方法获取
    app.config.from_object(config[config_name])
    # app初始化
    config[config_name].init_app(app)

    # 初始化扩展
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    # 导入并注册蓝本
    from .main  import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    
    return app
