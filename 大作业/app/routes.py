import flask
from requests import post
from app import app,db
from flask import render_template, flash, redirect, url_for, request,jsonify
from app.forms import LoginForm,RegistrationForm,EditProfileForm,PostForm,CommentForm

from flask_login import current_user, login_user,logout_user,login_required

from werkzeug.urls import url_parse # 处理next页面问题

from app.models import User,Post,Follow_Post

from datetime import datetime

from collections import OrderedDict

from hashlib import md5 # 生成MD5哈希值

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()




@app.route('/home', methods=['GET', 'POST'])
@login_required # 限制访问 只有登录后才能访问
def home():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user,lon=form.lon.data,lat=form.lat.data)
        db.session.add(post)
        db.session.commit()
        flash('帖子发表成功!')
        return redirect(url_for('home'))
    posts = current_user.followed_posts().all()
    #follow_post = Follow_Post.query.filter_by(post_id=2).all() # 测试 获取某一个一个帖子的所有跟帖
    follow_posts = Follow_Post.query.all()
    return render_template("home.html", title='主 页', form=form,
                           posts=posts,follow_posts=follow_posts)




@app.route('/login',methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated: # 先查询已登录用户表
        return redirect(url_for('home')) # 若用户已登录则直接返回home页面

    form = LoginForm() # 否则实例化表单类

    if form.validate_on_submit(): # 表单提交后开始查询数据库
        
        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(form.password.data):
        # 若未找到用户 或者密码错误 则闪现以下错误消息
            flash('用户名无效或密码错误')
            return redirect(url_for('login')) # 重定向至登录页面
        # 否则就登录用户 并缓存用户信息
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next') # 处理next字段参数 方便用户登录后返回该页面
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
        

    return render_template('login.html', title='登 录', form=form) # 首先返回表单页面


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home_map'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('恭喜！您已成功注册！')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

#     dsadasdasdas
@app.route('/user/<username>') # 用户主页
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    #posts = Post.query.filter_by(user_id=user.id).order_by(Post.timestamp.desc()).all()
    follow_posts = Follow_Post.query.filter_by(username=username).all()
    return render_template('user.html', user=user, posts=posts,follow_posts=follow_posts)



@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username) # 构造函数
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('user',username=current_user.username))# format.(current_user.username)
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


# 实现用户关注与取消关注

@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot follow yourself!')
        return redirect(url_for('user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are following {}!'.format(username))
    return redirect(url_for('user', username=username))

@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following {}.'.format(username))
    return redirect(url_for('user', username=username))


@app.route('/explore',methods=['GET', 'POST'])
@login_required
def explore(): # 正在测试评论组件
    comment_form = CommentForm() # 实例化用户评论类
    posts = Post.query.order_by(Post.timestamp.desc()).all() # 获取所有用户发帖表 并按时间排序
    if comment_form.validate_on_submit():
        if (comment_form.post_num.data <=0 or comment_form.post_num.data>Post.query.count()):
            flash("请输入正确的帖子编号！")
        else:
            follow_post = Follow_Post(body=comment_form.comment.data,
            landlord=Post.query.get(comment_form.post_num.data),
            username=current_user.username)
            db.session.add(follow_post)
            db.session.commit()
            flash('跟帖成功!')
            return redirect(url_for('explore'))

        
    return render_template('home.html', title='Explore', posts=posts,comment_form=comment_form)


# 接下来要针对地图开发出一套地址 实现数据的读写 跟帖等操作




@app.route('/')
@app.route('/home/mapview')
def home_map():
    return render_template('home_map.html')

@app.route('/login/mapview')
def login_map():
    return render_template('login_map.html')

@app.route('/user/mapview')
def user_map():
    return render_template('user_map.html')


@app.route('/explore/mapview')
def explore_map():
    return render_template('explore_map.html')

@app.route('/register/mapview')
def register_map():
    return render_template('register_map.html')

@app.route('/edit_profile/mapview')
def edit_profile_map():
    return render_template('edit_profile_map.html')



# 接下来是地图视图引擎的接口 地图与主业务逻辑是相互独立的关系 
    
def post_to_dict(post):
    return OrderedDict(
        user = post.author.username,
        lon = post.lon,
        lat = post.lat,
        content=post.body,
        digest = md5(post.author.username.lower().encode('utf-8')).hexdigest()
    )

@app.route('/JSON', methods = ['GET', 'POST'])# 返回数据库中所有记录的post数
@login_required # 只有登录才能看到所有的帖子
def get_json():
   return jsonify(list(map(post_to_dict, Post.query.all())))


@app.route('/map', methods = ['GET', 'POST'])# json数据绘制到地图上
def root_map():
    if request.method == 'POST':
      if not request.form['lon'] or not request.form['lat'] or not request.form['content']:
         flash('Please enter all the fields', 'error')
      else:
         post = Post(lon=request.form['lon'], lat=request.form['lat'],body=request.form['content'],author=current_user )
         db.session.add(post)
         db.session.commit()
         flash('Record was successfully added')
         return redirect(url_for('root_map'))
    return render_template('root_map.html')


'''
@app.route('/map', methods = ['GET', 'POST'])# json数据绘制到地图上
def map():
    return render_template('root_map.html')

'''


'''
 if request.method == 'POST':
      if not request.form['lon'] or not request.form['lat'] or not request.form['content']:
         flash('Please enter all the fields', 'error')
      else:
         post = Post(lon=request.form['lon'], lat=request.form['lat'],body=request.form['content'],author=current_user )
         db.session.add(post)
         db.session.commit()
         flash('Record was successfully added')
         return redirect(url_for('map'))
    elif request.method == 'GET':
'''

    
    

