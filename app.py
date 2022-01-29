from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource

from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////usr/src/app/database/database.db'
# mac / lunix -> absolute path 設法
# database 是 yo 在 docker 設的 working directory，也就是現在看到的根目錄
# sqlite:////usr/src/app/database/<filename>.py

db = SQLAlchemy(app)


jwt = JWTManager()
app.config['JWT_SECRET_KEY'] = 'sakura'  # 改成你設定的密鑰
jwt.init_app(app) # register this extension to your flask project
