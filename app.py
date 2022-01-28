from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from auth import Auth, Auth_login
from task import Task, Task_get

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////usr/src/app/database/database.db'
# mac / lunix -> absolute path 設法
# database 是 yo 在 docker 設的 working directory，也就是現在看到的根目錄
# sqlite:////usr/src/app/database/<filename>.py

db = SQLAlchemy(app)

api = Api(app)
api.add_resource( Auth,  "/auth/")
api.add_resource( Auth_login,  "/auth/login")
api.add_resource( Task, "/task/" )
api.add_resource( Task_get, "/task/<string:task_id>" ) # 將 task_id(uuid 發的，是 string) 傳給 Task_get function 作為 function 內 task_id 此變數的值



@app.route("/")
def home():
    return "Hello, World!"
