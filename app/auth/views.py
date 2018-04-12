import os
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_required, login_user, logout_user, current_user
from . import auth
from .forms import LoginForm, RegistrationFrom, ModifyPasswordForm, ModifyEmailForm
from ..models import User
from .. import db
from ..save import save_to_file

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
        user = User(username=form.username.data,
                email=form.email.data,
                password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        save_to_file(os.getenv('CONFIRM_PATH'),
                user.username, 'auth/email/confirm.html',
                user=user, token=token)
        flash('您需要确认后才能使用')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form = form)

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('您的账号已经确认')
    else:
        flash('无效的确认链接')
    return redirect(url_for('main.index'))

@auth.before_app_request
def before_request():
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.endpoint[:5] != 'auth.'\
            and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')

@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    save_to_file(os.getenv('CONFIRM_PATH'),
        current_user.username, 'auth/email/confirm.html',
        user=current_user, token=token)
    flash('新的确认邮件已经发送')
    return redirect(url_for('main.index'))

@auth.route('/profile')
@login_required
def profile():
   return render_template('auth/profile.html')

@auth.route('/profile/modify_password', methods=['GET', 'POST'])
@login_required
def modify_password():
    if current_user.confirmed:
        form = ModifyPasswordForm()
        if form.validate_on_submit():
            current_user.password = form.new_password.data
            db.session.add(current_user)
            db.session.commit()
            flash('密码修改成功，请重新登陆')
            logout_user()
            return redirect(url_for('auth.profile'))
        return render_template('auth/modify_password.html',form=form)
    return redirect(url_for('auth.unconfirmed'))

@auth.route('/profile/modify_email')
@login_required
def modify_email():
    token = current_user.generate_confirmation_token()
    save_to_file(os.getenv('CONFIRM_PATH'),
        current_user.email, 'auth/email/modify_email.html',
        user=current_user, token=token)
    return render_template('auth/modify_email.html')

@auth.route('profile/modify_email/<token>', methods=['GET', 'POST'])
@login_required
def confirm_modify_email(token):
    confirmation =  current_user.confirm(token)
    form = ModifyEmailForm()
    if form.validate_on_submit():
        current_user.email = form.email.data
        db.session.add(current_user)
        db.session.commit()
        flash('电子邮箱已修改')
        return redirect('auth/profile')
    return render_template('auth/confirm_modify_email.html', confirmation = confirmation, form = form)
