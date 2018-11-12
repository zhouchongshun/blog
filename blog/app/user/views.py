#针对用户业务逻辑处理的视图和路由的定义
from flask import render_template
# 导入蓝图程序，用于构建路由
from . import user
# 导入db用于操作数据库
from .. import db
# 导入实体类，用于操作实体类
from ..models import *

@user.route("/user")
def user_index():
    return "这是user程序包中的首页"

# @user.route("/index")
# def index_views():
#     return render_template("index.html")