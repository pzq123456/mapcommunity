from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
# 上面这些是引用外部的库

app = Flask(__name__)
# falsk的配置文件写在config类的属性中 在此处引用并写入其中
app.config.from_object(Config)

db = SQLAlchemy(app) # 数据库对象
migrate = Migrate(app, db) # 数据库迁移对象 方便无损更新数据库的结构

login = LoginManager(app) # 管理用户登录
login.login_view = 'login' # 处理只有用户登录和才可访问的视图


# 底部引用其他模块 防止重复引用
# 因为本来这些代码也是要写在 应用注册实例化之后的 下面的引用这些模块其实就相当于简单的把代码写在这下面
from app import routes, models ,errors
# 下面这些是引用自己编写的模块化的代码段