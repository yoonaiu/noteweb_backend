from app import app
import auth
import task

api = Api(app)
api.add_resource( auth.Auth,  "/auth/")
api.add_resource( auth.Auth_login,  "/auth/login")
api.add_resource( task.Task, "/task/" )
api.add_resource( task.Task_get, "/task/<string:task_id>" ) # 將 task_id(uuid 發的，是 string) 傳給 Task_get function 作為 function 內 task_id 此變數的值
