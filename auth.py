# self 有點像 this 的感覺
from email import message
from os import access
import app
from click import password_option
from flask_restful import Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from numpy import require
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, get_jwt, set_access_cookies, jwt_required
import uuid
import random

from datetime import datetime
from datetime import timedelta
from datetime import timezone


# 寫在參數列的東西是該韓式需要的東西，但應該不是到時候接收 json 資料報的接收方式

def get_salt():
    seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_ =-"
    sa = []  # list
    for i in range (10):
        sa.append( random.choice(seed) )

    salt = ''.join(sa)  # 把 sa list 內的元素用 '' 空字元連接起來，形成一個空字串存在 salt 裏面
    return salt

def check_name( name ):
    name_query = app.User.query.filter_by(name = name).first()
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

    @jwt_required   # 若是沒有提交token或是token內容有問題時會直接返還錯誤 -> 那還會有下面 401 的狀況嗎
    def get(self):  # 取得帳戶資訊，傳進來的會是 jwt, 用 jwt 去看就好，jwt 可看出 userid
        user_id = get_jwt_identity()
        query = app.User.query.filter_by(user_id = user_id).first()
        if query == None :
            return{
                'message' : 'token is not valid, unauthorized'
            }, 401

        else :
            return {
                'username' : query.name
            }, 200

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

        elif re2 == 422 :
            return {
                'message' : 'the password format is wrong'
            }, 422

        # 順利通過檢查就會來到這
        name = arg['name']
        salt = get_salt()
        hash_password = generate_password_hash(arg['password'] + salt)  # the default hash function is sha1 -> maybe not that safe (?, can change
        user_id = str(uuid.uuid4())

        app.db.session.add( app.User(user_id, name, hash_password, salt) )  # arg 從 json 擷取資訊
        app.db.session.commit()  # need to commit after change

        access_token = create_access_token(identity = user_id) # jwt
        return {
            'access_token' : access_token,
        }, 200


    @jwt_required  # 更新密碼，need jwt
    def put(self):
        arg = self.parser1.parse_args()
        new_password = arg['new_password'] # 串資料庫

        if check_password( new_password ) == 422 :
            return {
                'message' : 'the password format is wrong'
            }, 422

        user_id = get_jwt_identity()
        query = app.User.query.filter_by(user_id = user_id).first()
        if query == None :
            return {
                'message' : 'token is not valid, unauthorized'
            }, 401

        salt = query.salt  # use the original salt
        new_hash_password = generate_password_hash( new_password + salt )
        query.hash_password = new_hash_password
        app.db.session.commit()  # need to commit after change

        return {
            'message' : 'successfully change the password'
        }, 200

#   _
# /_+_\ there isn't space for UX improve here, name need to correct first than can know if the password is correct
# other filter the frontend can do
class Auth_login(Resource):

    parser1 = reqparse.RequestParser()
    parser1.add_argument( 'name', required = True ) # required / help 應該是前端會處理掉的東西，可以確定前端發過來的東西是通過標準符合格式的
    parser1.add_argument( 'password', required = True )

    def post(self): # login
        arg = self.parser1.parse_args()  # -> pass in name, password
        query = app.User.query.filter_by( name = arg['name'] ).first()

        if query == None :
            return {
                'message' : 'username does not exist'
            }, 401

        # username exist -> check the password
        salt = query.salt
        if check_password_hash( query.hash_password, arg['password'] + salt ) :
            # the name and the password are correct -> give the jwt (token)
            access_token = create_access_token( identity = query.user_id )
            return {
                'access_token' : access_token
            }, 200

        else :
            return {
                'message' : 'the password is incorrect'
            }, 401
