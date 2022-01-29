from flask_restful import Resource
from app import db

class Task (Resource): 
    def post(self, jwt, title, content):  # 新增一個 task，需要 user 的 jwt
        pass

    def put(self, jwt, new_title, new_content):     # 修改一個 task
        pass

    def delete(self, jwt, task_id): 
        pass


class Task_get (Resource):
    def get(self, jwt, task_id):
        pass