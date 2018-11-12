#主业务逻辑中的视图和路由定义
import datetime
import os

from flask import render_template, request, redirect,session
# 导入蓝图程序，用于构建路由
from pandas import json

from . import main
# 导入db用于操作数据库
from .. import db
# 导入实体类，用于操作实体类
from ..models import *

@main.route("/evis")
def main_index():
    categorys = Category.query.all()
    titles = Topic.query.limit(3).all()
    titles1 = Topic.query.limit(2).offset(3).all()
    titles2 = Topic.query.all()
    # for title in titles1:
    #     print(title.title)
    #查找id为1的user的信息
    # user = User.query.filter_by(id = 1).first()
    # print(user.uname)
    # topics = user.topics.all()
    # for topic in topics:
    #     print(topic.title+":"+topic.user.uname+":"+topic.category.cate_name+":"+topic.blogtype.type_name)
    if "uid" in session and "uname" in session:
        user = User.query.filter_by(id=session.get("uid")).first()
    return render_template("index.html",params=locals())
#登录
@main.route("/login",methods=["GET","POST"])
def login_views():
    if request.method == "GET":
        return render_template("login.html")
    else:
        # 接收前端传递回来的数据
        name = request.form.get("username")
        pwd = request.form.get("password")
        #使用接收的数据到数据库中查询
        user = User.query.filter(User.loginname==name,User.upwd==pwd).first()
        #如果用户存在，将信息保存在session并重定向会首页，否则重定向回登录页面
        if user:
            session["uid"] = user.id
            session["uname"] = user.uname
            return redirect("/")
        else:
            msg = "用户名或密码不正确"
            return render_template("login.html",errMsg=msg)
# 注册
@main.route("/register",methods=["GET","POST"])
def register_views():
    if request.method == "GET":
        return render_template("register.html")
    else:
        # 接收前端传递回来的数据
        loginname= request.form.get("loginname")
        uname = request.form.get("username")
        email = request.form.get("email")
        upwd = request.form.get("password")
        url = request.form.get("url")

        #使用接收的数据到数据库中查询
        user = User.query.filter_by(loginname=loginname).first()
        if user:
            msg = "账号已存在"
            return render_template("register.html",errMsg=msg)
        else:
            user = User(loginname,uname,email,url,upwd,0)
            # 将数据保存到数据库
            db.session.add(user)
            #手动提交，目的是为了获取提交之后的user的id
            db.session.commit()
            # 当user成功插入数据库之后，程序会自动将所有信息取出来再赋值给user
            session["uid"] = user.id
            session["uname"] = user.uname
            return  redirect("/")

#发布博客的访问路径
@main.route("/release",methods=["GET","POST"])
def release_views():
    if request.method == "GET":
        #验证用户是否有发表博客的权限即必须是登录用户，并且is_author的值必须是1
        if "uid" in session and "uname" in session:
            user = User.query.filter_by(id=session["uid"]).first()
            if user.is_author:
                categorys = Category.query.all()
                blogTypes = BlogType.query.all()
                return render_template("release.html",params=locals())
            else:
                return redirect("/")
        else:
            return redirect("/login")
    else:
        #处理post请求即发表博客的处理
        topic = Topic()
        # 为title赋值
        topic.title = request.form.get("author")
        #为blogtype_id赋值
        topic.blogtype_id = request.form.get("list")
        #为category_id赋值
        topic.category_id = request.form.get("category")
        #为user_id赋值
        topic.user_id = session.get("uid")
        #为content赋值
        topic.content = request.form.get("content")
        #为pub_date赋值
        topic.pub_date = datetime.datetime.now().strftime("%Y-%m-%d")
        # print(topic.title,topic.blogtype_id,topic.category_id,topic.user_id,topic.content)
        #为选择性的images赋值
        if request.files:
            # print("有文件上传")
            #取出文件
            f = request.files.get('picture')
            #处理文件名称，将名称赋值给topic.images
            ftime = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
            ext = f.filename.split(".")[1]
            filename = ftime + "." + ext
            # print(f.filename)
            topic.images = "upload/" + filename
            #将文件保存至服务器
            # os.path.dirname(__file__)得到当前文件views所在目录main
            # os.path.dirname(os.path.dirname(__file__))当前文件views所在目录main的上级目录app
            path_upload = os.path.dirname(os.path.dirname(__file__))
            lst = path_upload.split('/')
            lst.append('static')
            lst.append('upload')
            path_upload = '\\'.join(lst)
            filename = os.path.join(path_upload, filename)
            print(filename)
            f.save(filename)
        else:
            print("文件没有上传")
        db.session.add(topic)
        return redirect("/")

#退出的访问路径
@main.route("/logout")
def loginout_views():
    if "uid" in session and "uname" in session:
        del session["uid"]
        del session["uname"]
    return redirect("/")

@main.route("/info",methods=["GET","POST"])
def info_views():
    if request.method == "GET":
        #查询要看的博客的信息
        topic_id = request.args.get("topic_id")
        topic = Topic.query.filter_by(id=topic_id).first()
        #更新阅读量
        topic.read_num = int(topic.read_num) + 1
        db.session.add(topic)
        #查找上一篇以及下一篇
        #上一篇：查询topic.id比当前topic_id小的最后一条数据
        prevTopic = Topic.query.filter(Topic.id<topic_id).order_by("id desc").first()
        # print(prevTopic)
        #下一篇：查询topic_id比当topic_id大的第一条数据
        nextTopic = Topic.query.filter(Topic.id>topic_id).first()
        # print(nextTopic)
        #查询登录用户
        if "uid" in session and "uname" in session:
            user = User.query.filter_by(id=session["uid"])
        return render_template("info.html",params=locals())




