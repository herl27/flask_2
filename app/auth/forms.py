from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User

class LoginForm(FlaskForm):
    email = StringField('电子邮件', validators=[DataRequired(), Length(1, 64),
        Email('请输入有效的邮箱地址')])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('保存登录信息')
    submit = SubmitField('提交')

class RegistrationFrom(FlaskForm):
    email = StringField('电子邮件', validators=[DataRequired(), Length(1, 64),
        Email('请输入有效的邮箱地址')])
    username = StringField('用户名', validators=[DataRequired(), Length(1, 64),
        Regexp("^[A-Za-z][A-Za-z0-9\_]*$", flags=0, message= "用户名只能以字母开头，且只能包含字母、数字和下划线")])
    password = PasswordField("密码", validators=[DataRequired(), EqualTo('password2',
        message="两次密码不一致")])
    password2 = PasswordField("确认密码", validators=[DataRequired()])
    submit = SubmitField("注册")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已被注册')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已经注册')
            
class ModifyPasswordForm(FlaskForm):
    old_password = PasswordField('旧密码', validators=[DataRequired()])
    new_password = PasswordField('新密码', validators=[DataRequired(),
                                    EqualTo('new_password2', message='两次密码不一致')])
    new_password2 = PasswordField('确认新密码', validators=[DataRequired()])
    submit = SubmitField("更改密码")

    def validate_old_password(self, field):
        if not current_user.verify_password(field.data):
            raise ValidationError('密码错误')

