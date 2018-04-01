# 蓝本中的程序路由（视图函数）
from datetime import datetime
from flask import render_template, session, redirect, url_for

from . import main
from forms import NameForm

# rote注册在蓝本中
@main.route('/', ['GET', 'POST')
def index():
    form = NameForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        # urlfor()需要指定蓝本的名字，当前蓝本可简写
        return redirect(url_for('.index'))
    return render_template('index.html', 
        name=session[name], 
        current_time = datetime.utcnow())
