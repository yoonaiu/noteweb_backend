from app.db import db


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
