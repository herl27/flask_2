from . import db, login_manager
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime
import hashlib

# 定义权限常量
class Permission(object):
    # 关注用户
    FOLLOW = 0x01
    # 发表评论
    COMMENT = 0x02
    # 发表文章
    WRITE_ARTICLES = 0x04
    # 审核评论
    MODERATE_COMMENTS = 0x08
    # 管理权限
    ADMINISTER = 0x80
    
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role')
    def __repr__(self):
        return '<Role %r>' % self.name

    @staticmethod
    def insert_roles():
        roles = {
                'User': (Permission.FOLLOW |
                         Permission.COMMENT |
                         Permission.WRITE_ARTICLES, True),
                'Moderator': (Permission.FOLLOW |
                              Permission.COMMENT |
                              Permission.WRITE_ARTICLES |
                              Permission.MODERATE_COMMENTS, False),
                'Administrator': (0xff, False)
                }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text)
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    gravatar_hash = db.Column(db.String(32))

    def __repr__(self):
        return '<Role %r>' % self.username

    # User 类的构造函数首先调用基类的构造函数，
    # 如果创建基类对象后还没定义角色，
    # 则根据电子邮件地址决定将其设为管理员还是默认角色。
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        # 检测是否已经指定权限
        if self.role is None:
            # 检查邮箱是否和FLASKY_ADMIN中的一致
            if self.email == current_app.config['FLASKY_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            # 若还是没有设置权限则自动设置默认权限
            if self.role is None:
                # 通过指定默认值的方法比较容易修改默认权限(猜测)
                self.role = Role.query.filter_by(default=True).first()
        # 生成头像hash
        if self.email is not None and self.gravatar_hash is None:
            self.gravatar_hash = hashlib.md5(
                    self.email.encode('utf-8')).hexdigest()

    # 密码支持
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # 用户认证
    def generate_confirmation_token(self, expiration=600):
        s = Serializer(current_app.config.get('SECRET_KEY'), expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config.get('SECRET_KEY'))
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        db.session.commit()
        return True

    # 更改电子邮件并更新头像hash
    def change_email(self, new_email):
        self.email = new_email
        self.gravatar_hash = hashlib.md5(
                self.email.endcode('utf-8')).hexdigest()
        db.session.add(self)
        db.commit()

    # 为了简化角色和权限的实现过程，
    # 我们可在User 模型中添加一个辅助方法，检查是否有指定的权限
    def can(self, permissions):
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    # 用于刷新记录用户访问网站日期的last_seen字段，该方法于auth.beforre_request中调用
    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def gravatar(self, size=100, rating='g', default='wavatar'):
        url = 'https://cdn.v2ex.com/gravatar/'
        hash = self.gravatar_hash or hashlib.md5(
                self.email.encode('utf-8')).hexdigest()
        return '{url}{hash}?s={size}&r={rating}&d={default}'.format(
               url=url, hash=hash, size=size, rating=rating, default=default)
# 出于一致性考虑，我们还定义了AnonymousUser 类，并实现了can() 方法和is_administrator()
# 方法。这个对象继承自Flask-Login 中的AnonymousUserMixin 类，并将其设为用户未登录时
# current_user 的值。这样程序不用先检查用户是否登录，就能自由调用current_user.can() 和
# current_user.is_administrator()
class AnonymousUser(AnonymousUserMixin):

    def can(self, permissisons):
        return False
    
    def is_administrator(self):
        return False

# login_manager.anoumous_user = AnonymousUser
# 出于一致性考虑，将其放到__init__.py中

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
