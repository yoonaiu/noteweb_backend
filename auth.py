# self 有點像 this 的感覺
from flask_restful import Resource, reqparse
from numpy import require

# 寫在參數列的東西是該韓式需要的東西，但應該不是到時候接收 json 資料報的接收方式

class Auth (Resource): # 目前理解：函式參數列表明希望收到哪些條件以便處理，但不一定要是從網址傳進來的，可能也可以是 json 形式的資料報
    
    # post 會用到的東西，原本的寫法 :
    # 不是很確定為甚麼會用到 parser, 不能直接用參數傳入嗎～～ -> 還是寫在函式參數列的東西只能是用網址傳入的東西
    # 所以如果是 json or form 發過來的東西就要用 parser 接
    parser1 = reqparse.RequestParser() 
    parser1.add_argument( 'name', required = True ) # required / help 應該是前端會處理掉的東西，可以確定前端發過來的東西是通過標準符合格式的
    parser1.add_argument( 'password', required = True )
    
    parser2 = reqparse.RequestParser() 
    parser2.add_argument( 'new_password', required = True )
    
    
    def get(self, jwt):  # 取得帳戶資訊，傳進來的會是 jwt, 用 jwt 去看就好，jwt 可看出 userid
        pass

    def post(self): # register 一個帳戶
        arg = self.parser1.parse_args() # 處理前端發來的 json request -> name, password
        user = {  # 這邊應該要串資料庫，還沒串
            'name' : arg['name'], # 擷取 json 中的資訊
            'password' : arg['password']
        }
        

    def put(self, jwt):  # 更新密碼，need jwt
        arg = self.parser1.parse_args()
        arg['new_password'] # 串資料庫
        

class Auth_login(Resource):
    def post(self, name, password): # 登入
        pass

