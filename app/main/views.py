# 蓝本中的程序路由（视图函数）
from datetime import datetime
from flask import render_template, session, redirect, url_for

from . import main
from .forms import NameForm
from .. import db
from ..models import User
# route注册在蓝本中
@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        user = User.query.filter_by(username=form.name.data).first()
        if user:
            session['known'] = True
        else:
            session['known'] = False
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()         
        # urlfor()需要指定蓝本的名字，当前蓝本可简写
        return redirect(url_for('.index'))
    return render_template('index.html', form=form,
        name=session.get('name'), known=session.get('known'),
        current_time = datetime.utcnow())
