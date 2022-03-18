from flask import Flask
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource

from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, get_jwt, set_access_cookies

from app.resources.user import Auth, Auth_login
from app.resources.task import Task, Task_get

import config

from datetime import datetime
from datetime import timedelta
from datetime import timezone

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/yoona/Documents/noteweb_backend/database.db' # do not use ~/Document

# mac / lunix -> absolute path 設法
# database 是 yo 在 docker 設的 working directory，也就是現在看到的根目錄
# sqlite:////usr/src/app/database/<filename>.py

# use this method to avoid circular import
# done create_all
@app.before_first_request
def create_tables():
    from app.db import db   
    db.init_app(app)
    db.create_all()


api = Api(app)
api.add_resource( Auth,  "/auth/")
api.add_resource( Auth_login,  "/auth/login")
api.add_resource( Task, "/task/" )
api.add_resource( Task_get, "/task/<string:task_id>" ) # 將 task_id(uuid 發的，是 string) 傳給 Task_get function 作為 function 內 task_id 此變數的值


jwt = JWTManager()
app.config['JWT_SECRET_KEY'] = config.jwt_secret_key  # 改成你設定的密鑰
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1) # 設 jwt expire time 為 1 小時
jwt.init_app(app) # register this extension to your flask project


# token 重發還沒處理好 -> 要怎麼讓前端接住新的 token
@app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
            #return {
            #    'access_token' : access_token
            # }, 200
        else:
            return response

    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original respone
        return response

'''
@jwt.expired_token_loader
def my_expired_token_callback(jwt_header, jwt_payload):
    print("hello\n\n\n")
    return jsonify(code = "meanless", err = "the token is expired"), 401

@jwt.invalid_token_loader
def my_invalid_token_loader_callback(reason):
    return jsonify(invalid_reason = reason), 401
'''


if __name__ == '__main__':
    app.run( debug = True )
