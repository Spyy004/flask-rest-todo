from typing_extensions import Required
from flask import Flask
from flask_restful import Resource, Api, marshal_with, reqparse, abort, fields
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
db = SQLAlchemy(app)

class ToDoModel(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    task = db.Column(db.String(200))
    summary = db.Column(db.String(200))
db.create_all()
task_post_args = reqparse.RequestParser()
task_post_args.add_argument("task",type=str,help="Task is required",required = True)
task_post_args.add_argument("summary",type=str,help="Summary is required",required = True)

resource_fields = {
    'id':fields.Integer,
    'summary':fields.String,
    'task':fields.String
}
class ToDo(Resource):
    @marshal_with(resource_fields)
    def get(self,todo_id):
        task = ToDoModel.query.filter_by(id=todo_id).first()
        if not task: 
            abort(404,message="Could not find task with that id")
        return task
    @marshal_with(resource_fields)
    def post(self,todo_id):
        args = task_post_args.parse_args()
        task = ToDoModel.query.filter_by(id=todo_id).first()
        if task:
            abort(409,description="Already Present")
        todo = ToDoModel(id=todo_id,task=args['task'],summary=args['summary'])
        db.session.add(todo)
        db.session.commit()
        return todo, 201
    def delete(self,todo_id):
         task = ToDoModel.query.filter_by(id=todo_id).first()
         db.session.delete(task)
         return 'Todo Deleted', 204
class ToDoList(Resource):
    def get(self):
        tasks = ToDoModel.query.all()
        todos = {}
        for task in tasks:
            todos[task.id] = {"task":task.task,"summary":task.summary}
        return todos
api.add_resource(ToDo,'/todos/<int:todo_id>')
api.add_resource(ToDoList,'/todos')
if __name__ == '__main__':
    app.run(debug=True)