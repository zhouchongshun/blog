#当前项目相关的模型文件，即所有的实体类

from . import db

class Category(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer,primary_key=True)
    cate_name = db.Column(db.String(50),nullable=False)

    #增加反向引用，引用topic表
    topics = db.relationship("Topic",backref=("category"),lazy="dynamic")

class BlogType(db.Model):
    __tablename__ = "blogtype"
    id = db.Column(db.Integer,primary_key=True)
    type_name = db.Column(db.String(20),nullable=False)

    #增加反向引用，引用topic表
    topics = db.relationship("Topic",backref=("blogtype"),lazy="dynamic")


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer,primary_key=True)
    loginname = db.Column(db.String(50),nullable=False)
    uname = db.Column(db.String(30),nullable=False)
    email = db.Column(db.String(200),nullable=False)
    url = db.Column(db.String(200))
    upwd = db.Column(db.String(30),nullable=False)
    is_author = db.Column(db.SmallInteger,default=0)

    #增加反向引用，引用topic表
    topics = db.relationship("Topic",backref=("user"),lazy="dynamic")
    #增加反向引用，引用reply表
    replys = db.relationship("Reply",backref=("user"),lazy="dynamic")
    #增加与topic之间的关联关系和反向引用
    voke_topics = db.relationship(
        "Topic",
        secondary="voke",
        backref=db.backref("voke_users",lazy="dynamic"),
        lazy="dynamic"
    )
    def __init__(self,loginname,uname,email,url,upwd,is_author):
        self.loginname = loginname
        self.uname = uname
        self.email = email
        self.url = url
        self.upwd = upwd
        self.is_author = is_author

class Topic(db.Model):
    __tablename__ = "topic"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200),nullable=False)
    pub_date = db.Column(db.DateTime,nullable=False)
    read_num = db.Column(db.Integer,default=0)
    content = db.Column(db.Text,nullable=False)
    images = db.Column(db.Text)

    #创建外键，引用主键表blogtype的键id
    blogtype_id = db.Column(db.Integer,db.ForeignKey("blogtype.id"))
    #创建主键，引用主键表categroy
    category_id = db.Column(db.Integer,db.ForeignKey("category.id"))
    #创建主键，引用主键表user
    user_id = db.Column(db.Integer,db.ForeignKey("user.id"))
    #增加反向引用，引用reply表
    replys = db.relationship("Reply",backref=("topic"),lazy="dynamic")


class Reply(db.Model):
    __tablename__ = "reply"
    id = db.Column(db.Integer,primary_key=True)
    content = db.Column(db.Text,nullable=False)
    reply_time = db.Column(db.DateTime)

    #关系：一（Topic）对多（Reply）的关系
    topic_id = db.Column(db.Integer,db.ForeignKey("topic.id"))
    #关系：一（User）对多（Reply）的关系
    user_id = db.Column(db.Integer,db.ForeignKey("user.id"))

Voke = db.Table(
    "voke",
    db.Column("id",db.Integer,primary_key=True),
    db.Column("user_id",db.Integer,db.ForeignKey("user.id")),
    db.Column("topic_id",db.Integer,db.ForeignKey("topic.id"))
)