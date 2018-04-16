# 蓝本
# 在蓝本中定义的路由处于休眠状态，直到蓝本注册到程序上后，路由才真正成为程序
# 的一部分。使用位于全局作用域中的蓝本时，定义路由的方法几乎和单脚本程序一样。
from flask import Blueprint

main = Blueprint('main', __name__)

# 程序的路由保存在包里的app/main/views.py
# 错误处理程序保存在app/main/errors.py
# 把路由和错误处理程序与蓝本关联起来
# "from ." 代表从当前包中导入
from . import views, errors

from ..models import Permission

@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)
