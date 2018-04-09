from flask import render_template, redirect, request, url_for, flash
from flask_login import login_required, login_user, logout_user
from . import auth
from .forms import LoginForm, RegistrationFrom
from ..models import User
from .. import db

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
           login_user(user, remember=form.remember_me.data)
           return redirect(request.args.get('next') or url_for('main.index'))
        flash('错误的用户名或密码')
    return render_template('auth/login.html',form=form)

@auth.route('/secret')
@login_required
def secret():
    return 'Only authenticated users are allowed!'

@auth.route('/logout')
@login_required
def logout():
   logout_user()
   flash('账号已经退出登陆')
   return redirect(url_for('main.index'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationFrom()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('注册成功，您可以登陆了')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form = form)
