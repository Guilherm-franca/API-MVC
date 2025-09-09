from flask_restx import Namespace, Resource, fields
from flask import request
from models.task import Task
from models.user import Usuario
from database import db

task_ns = Namespace('tasks', description='Operações relacionadas a tarefas')

task_model = task_ns.model('Task', {
    'id': fields.Integer(readonly=True, example=1),
    'title': fields.String(required=True, example='Comprar leite'),
    'description': fields.String(example='Ir ao supermercado comprar leite'),
    'status': fields.String(example='Pendente'),
    'user_id': fields.Integer(required=True, example=2),
})

task_create_model = task_ns.model('TaskCreate', {
    'title': fields.String(required=True, example='Comprar leite'),
    'description': fields.String(example='Ir ao supermercado comprar leite'),
    'user_id': fields.Integer(required=True, example=2),
})

@task_ns.route('')
class TaskList(Resource):
    @task_ns.marshal_list_with(task_model)
    def get(self):
        """Listar todas as tarefas"""
        tasks = Task.query.all()
        return tasks

    @task_ns.expect(task_create_model, validate=True)
    @task_ns.marshal_with(task_model, code=201)
    def post(self):
        """Criar uma nova tarefa"""
        data = request.json
        user = Usuario.query.get(data['user_id'])
        if not user:
            task_ns.abort(404, "Usuário não encontrado")

        new_task = Task(
            title=data['title'],
            description=data.get('description', ''),
            user_id=data['user_id']
        )
        db.session.add(new_task)
        db.session.commit()
        return new_task, 201

@task_ns.route('/<int:task_id>')
@task_ns.param('task_id', 'ID da tarefa')
class Task(Resource):
    @task_ns.marshal_with(task_model)
    def get(self, task_id):
        """Obter uma tarefa pelo ID"""
        task = Task.query.get_or_404(task_id, "Tarefa não encontrada")
        return task

    @task_ns.expect(task_create_model, validate=True)
    @task_ns.marshal_with(task_model)
    def put(self, task_id):
        """Atualizar uma tarefa"""
        task = Task.query.get_or_404(task_id, "Tarefa não encontrada")
        data = request.json

        task.title = data['title']
        task.description = data.get('description', task.description)
        task.user_id = data['user_id']

        db.session.commit()
        return task

    def delete(self, task_id):
        """Excluir uma tarefa"""
        task = Task.query.get_or_404(task_id, "Tarefa não encontrada")
        db.session.delete(task)
        db.session.commit()
        return {'message': 'Tarefa excluída com sucesso'}, 200