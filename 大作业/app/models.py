from app import db
from datetime import datetime # 获取时间戳 用以对用户发帖进行排序
from werkzeug.security import generate_password_hash, check_password_hash # 哈希加密用户密码
from flask_login import UserMixin # flask-login的数据库依赖
from app import login # 用户加载函数
from hashlib import md5 # 生成MD5哈希值


# 该模块用以定义数据库及相关操作
@login.user_loader
def load_user(id):
    return User.query.get(int(id)) # 配置一个用户加载函数 可以调用该函数来加载给定ID的用户

# 实现粉丝（关注）机制 关系的关联表 并非实体模型
followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
) # 左侧用户关注右侧用户

class User(UserMixin,db.Model): # UserMixin包含一些login库的依赖字段
    id = db.Column(db.Integer, primary_key=True) # 主键 自动添加
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128)) #使用哈希密码 防止数据库被盗取 明文密码盗用
    posts = db.relationship('Post', backref='author', lazy='dynamic') # 一对多 外键 连接到用户的帖子
    # 充实用户信息的字段
    about_me = db.Column(db.String(140)) 
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    # 实现粉丝机制
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic') # lazy：设置为动态模式的查询不会立即执行，直到被调用
    

    def __repr__(self): # 该方法用于在调试时打印数据库表
        return '<User {}>'.format(self.username)    

    def set_password(self, password):
        self.password_hash = generate_password_hash(password) # 生成哈希密码

    def check_password(self, password):
        return check_password_hash(self.password_hash, password) # 对比哈希密码

    def avatar(self, size): # 用户头像管理函数
        digest = md5(self.username.lower().encode('utf-8')).hexdigest()
        return 'https://gravatar.loli.net/avatar/{}?d=identicon&s={}'.format(
            digest, size) # 向gravatar.com网站请求随机头像 源网站国内无法快速访问 所以采用镜像网站

    def follow(self, user): # 关注
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user): # 取消关注
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user): # 判断该用户是否已经被关注
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())


class Post(db.Model): # 用户发帖表

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String()) # 帖子的主要内容
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow) # 发帖时间戳
    ######地理社区的新内容######
    lon = db.Column(db.Float())  #经度
    lat = db.Column(db.Float())  #纬度
    ######地理社区的新内容#####
    follow_posts=db.relationship('Follow_Post', backref='landlord', lazy='dynamic') # 一对多 外键 连接到楼主的帖子
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # 外键与发帖用户相关联
    

    def __repr__(self): # 该方法用于在调试时打印数据库表
        return '<Post {}>'.format(self.body)
 

class Follow_Post(db.Model): # 用户跟帖表
    id = db.Column(db.Integer, primary_key=True) # 自动主键
    body = db.Column(db.String(140)) # 跟帖内容限制长度
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow) # 跟帖时间戳
    username = db.Column(db.String(64)) # 跟帖用户名 为方便日后展示跟帖内容 这里直接写入用户名
    # 记录的是发送此帖子的用户名
    post_id = db.Column(db.Integer, db.ForeignKey('post.id')) # 外键与帖子编号相关联

    def __repr__(self): # 该方法用于在调试时打印数据库表
        return '<Follow_Post {}>'.format(self.body)

    def avatar(self, size): # 用户头像管理函数
        digest = md5(self.username.lower().encode('utf-8')).hexdigest()
        return 'https://gravatar.loli.net/avatar/{}?d=identicon&s={}'.format(
            digest, size) # 向gravatar.com网站请求随机头像 源网站国内无法快速访问 所以采用镜像网站
    # 利用用户名向国内的镜像网站请求头像服务

