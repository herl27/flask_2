# 表单对象
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, Regexp
from ..models import User, Role

class NameForm(FlaskForm):
    name = StringField("你是谁：",validators=[DataRequired()])
    submit = SubmitField("提交")

class EditProfileForm(FlaskForm):
    username = StringField('用户名',render_kw={'disabled': True})
    name = StringField('姓名', validators=[Length(0, 64)])
    location = StringField('地址', validators=[Length(0, 64)])
    about_me = TextAreaField('自我介绍')
    submit = SubmitField('修改')

class EditProfileAdminForm(FlaskForm):
    email = StringField('电子邮件', validators=[DataRequired(), Length(1, 64),
        Email('请输入有效的邮箱地址')])
    username = StringField('用户名', validators=[DataRequired(), Length(1, 64),
        Regexp("^[A-Za-z][A-Za-z0-9\_]*$", flags=0, message= "用户名只能以字母开头，且只能包含字母、数字和下划线")])
    confirmed = BooleanField('已确认')
    name = StringField('姓名', validators=[Length(0, 64)])
    location = StringField('地址', validators=[Length(0, 64)])
    role = SelectField('权限', coerce=int)
    about_me = TextAreaField('自我介绍')
    submit = SubmitField('修改')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                                for role in Role.query.order_by(Role.name).all()] 
        self.user = user
    # 首先检查字段的值是否发生了变化，如果有变化则验证，保证新值和先有的值不重复
    def validate_email(self, field):
        if field.data != self.user.email and \
            User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已被注册')

    def validate_username(self, field):
        if field.data != self.user.username and \
             User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已经注册')
 
