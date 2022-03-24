from app.db import db


class UserModel( db.Model ):
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


    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def save_change_to_db(self):
        db.session.commit()


    # add other needed function here, and import above





    # document 不是 primary key 的地方沒有特別設為 False
    # 一個 user 對多個 task
    # Class 名 / table 名 使用時機 ?
    # db.String(size) 都要指定長度 -> 更新 document
