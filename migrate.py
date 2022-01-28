# table & create all
# flask 的東西是放在另外一邊
# document 不是 primary key 的地方沒有特別設為 False
# 一個 user 對多個 task
# Class 名 / table 名 使用時機 ?
# db.String(size) 都要指定長度 -> 更新 document
# uuid 生的字串應該長 32

from app import app, db
import uuid

class User( db.model ):
    __tablename__ = 'user'
    user_id = db.Column(db.string(32), primary_key = True, unique = True, nullable = False)
    name = db.Column(db.String(30), unique = True, nullable = False)
    password = db.Column(db.String(64), unique = False, nullable = False)
    salt = db.Column(db.String(10), unique = False, nullable = False)
    
    # 一對多的一 -> 設定 relationship
    # 未來在讀 task 表格時，就可以用 Task.user 讀到 user 內的資料了
    db_user_task = db.relationship("Task", backref="user")

    def __init__(self, user_id, name, password, salt) :  # 初始化沒有 task_id
        self.user_id = user_id
        self.name = name
        self.password = password
        self.salt = salt




class Task( db.model ):
    __tablename__ = 'task'
    task_id = db.Column(db.string(32), primary_key = True, unique = True, nullable = False)
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



# creat all 還沒做


