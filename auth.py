# self 有點像 this 的感覺
from app import db, User, Task
from click import password_option
from flask_restful import Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from numpy import require
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager
import uuid
import random

# 寫在參數列的東西是該韓式需要的東西，但應該不是到時候接收 json 資料報的接收方式

def get_salt():
    seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_ =-"
    sa = []  # list
    for i in range (10):
        sa.append( random.choice(seed) )

    salt = ''.join(sa)  # 把 sa list 內的元素用 '' 空字元連接起來，形成一個空字串存在 salt 裏面
    return salt

def check_name( name ):
    name_query = User.query.filter_by(name = name).first()
    if name_query != None :   # 如果已經存在 -> 409 return
        return 409
    elif ( not name.isalnum() ) or ( len(name) > 30 ) :
        return 422
    else :
        return 200


def check_password( password ):
    if len(password) < 6 or len(password) > 30 :
        return 422


class Auth (Resource): # 目前理解：函式參數列表明希望收到哪些條件以便處理，但不一定要是從網址傳進來的，可能也可以是 json 形式的資料報

    # post 會用到的東西，原本的寫法 :
    # 不是很確定為甚麼會用到 parser, 不能直接用參數傳入嗎～～ -> 還是寫在函式參數列的東西只能是用網址傳入的東西
    # 所以如果是 json or form 發過來的東西就要用 parser 接
    # name, password 格式預設先用前端處理掉，後端只看有沒有重複
    parser1 = reqparse.RequestParser()
    parser1.add_argument( 'name', required = True ) # required / help 應該是前端會處理掉的東西，可以確定前端發過來的東西是通過標準符合格式的
    parser1.add_argument( 'password', required = True )

    parser2 = reqparse.RequestParser()
    parser2.add_argument( 'new_password', required = True )


    def get(self, jwt):  # 取得帳戶資訊，傳進來的會是 jwt, 用 jwt 去看就好，jwt 可看出 userid
        pass

    def post(self): # register 一個帳戶
        arg = self.parser1.parse_args()  # 處理前端發來的 json request -> name, password
        re1 = check_name( arg['name'] )
        re2 = check_password( arg['password'] )

        if re1 == 409 :
            return {
                'message' : 'the username has already been taken'
            }, 409  # 409 寫這邊應該是會回傳的ㄅ -> 不知道怎麼回傳的
        elif re1 == 422 :
            return {
                'message' : 'the username format is wrong'
            }, 422
        elif check_password == 422 :
            return {
                'message' : 'the password format is wrong'
            }, 422

        # 順利通過檢查就會來到這
        name = arg['name']
        salt = get_salt()
        hash_password = generate_password_hash(arg['password'] + salt)
        user_id = str(uuid.uuid4())

        db.session.add( User(user_id, name, hash_password, salt) )  # arg 從 json 擷取資訊
        access_token = create_access_token(identity = user_id) # jwt
        return {
            'access_token' : access_token
        }, 200


    def put(self, jwt):  # 更新密碼，need jwt
        arg = self.parser1.parse_args()
        arg['new_password'] # 串資料庫


class Auth_login(Resource):
    def post(self, name, password): # 登入
        pass
