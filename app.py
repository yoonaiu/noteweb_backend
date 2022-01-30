from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource

from flask_jwt_extended import JWTManager
import auth
import task

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////usr/src/app/database/database.db'
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
app.config['JWT_SECRET_KEY'] = 'sakura'  # 改成你設定的密鑰
jwt.init_app(app) # register this extension to your flask project
