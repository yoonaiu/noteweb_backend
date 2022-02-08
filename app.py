from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource

from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, get_jwt, set_access_cookies
import auth
import task
import config

from datetime import datetime
from datetime import timedelta
from datetime import timezone

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/yoona/Documents/noteweb_backend/database/database.db' # do not use ~/Document

# mac / lunix -> absolute path 設法
# database 是 yo 在 docker 設的 working directory，也就是現在看到的根目錄
# sqlite:////usr/src/app/database/<filename>.py

db = SQLAlchemy(app)

api = Api(app)
api.add_resource( auth.Auth,  "/auth/")
api.add_resource( auth.Auth_login,  "/auth/login")
api.add_resource( task.Task, "/task/" )
api.add_resource( task.Task_get, "/task/<string:task_id>" ) # 將 task_id(uuid 發的，是 string) 傳給 Task_get function 作為 function 內 task_id 此變數的值


jwt = JWTManager()
app.config['JWT_SECRET_KEY'] = config.jwt_secret_key  # 改成你設定的密鑰
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1) # 設 jwt expire time 為 1 小時
jwt.init_app(app) # register this extension to your flask project


@app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            # set_access_cookies(response, access_token)
            return {
                'access_token' : access_token,
            }, 200
        else:
            return response

    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original respone
        return response


# table & create all
# flask 的東西是放在另外一邊
# document 不是 primary key 的地方沒有特別設為 False
# 一個 user 對多個 task
# Class 名 / table 名 使用時機 ?
# db.String(size) 都要指定長度 -> 更新 document
# uuid 生的字串應該長 32

# from app import app, db
import uuid

class User( db.Model ):
    __tablename__ = 'user'
    user_id = db.Column(db.String(32), primary_key = True, unique = True, nullable = False)
    name = db.Column(db.String(30), unique = True, nullable = False)
    hash_password = db.Column(db.String(64), unique = False, nullable = False)
    salt = db.Column(db.String(10), unique = False, nullable = False)

    # 一對多的一 -> 設定 relationship
    # 未來在讀 task 表格時，就可以用 Task.user 讀到 user 內的資料了
    db_user_task = db.relationship("Task", backref="user")

    def __init__(self, user_id, name, hash_password, salt) :  # 初始化沒有 task_id
        self.user_id = user_id
        self.name = name
        self.hash_password = hash_password
        self.salt = salt




class Task( db.Model ):
    __tablename__ = 'task'
    task_id = db.Column(db.String(32), primary_key = True, unique = True, nullable = False)
    title = db.Column(db.String(30), unique = True, nullable = False)
    content = db.Column(db.String(5000), unique = False, nullable = False)

    # task 中的 user_id 可以不唯一（？ -> 可能很多個 task 是同一個主人
    # 兩張表連結時，用 user id 作為 key 去 user 的 table 找資料
    # 在 task 中找 user 的資料（？ -> 找特定 user 的資料就用 user id 在 task 的 table 內篩特定 user 的 task
    user_id_of_task = db.Column(db.String, db.ForeignKey('user.user_id'), primary_key = False, unique = False, nullable = False)

    def __init__(self, task_id, title, content, user_id_of_task) :  # 初始化沒有 task_id
        self.task_id = task_id
        self.title = title
        self.content = content
        self.user_id_of_task = user_id_of_task



# creat all 還沒做 -> 在外面 creat all
