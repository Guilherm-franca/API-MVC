from flask import jsonify, request
from models.task import Task
from models.user import Usuario
from database import db


class TaskController:
    @staticmethod
    def list_tasks():
        tasks = Task.query.all()
        tasks_data = [
            {
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'status': task.status,
                'user_id': task.user_id
            } for task in tasks
        ]
        return jsonify(tasks=tasks_data), 200

    @staticmethod
    def create_task():
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Request body must be JSON'}), 400

        title = data.get('title')
        description = data.get('description', '')
        user_id = data.get('user_id')

        if not title or not user_id:
            return jsonify({'error': 'title and user_id are required'}), 400

        user = Usuario.query.get(user_id)
        if not user:
            return jsonify({'error': 'User  not found'}), 404

        new_task = Task(title=title, description=description, user_id=user_id)
        db.session.add(new_task)
        db.session.commit()

        return jsonify({
            'message': 'Task created successfully',
            'task': {
                'id': new_task.id,
                'title': new_task.title,
                'description': new_task.description,
                'status': new_task.status,
                'user_id': new_task.user_id
            }
        }), 201

    @staticmethod
    def update_task_status(task_id):
        task = Task.query.get(task_id)
        if not task:
            return jsonify({'error': 'Task not found'}), 404


        task.status = 'Concluído' if task.status == 'Pendente' else 'Pendente'
        db.session.commit()

        return jsonify({
            'message': 'Task status updated',
            'task': {
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'status': task.status,
                'user_id': task.user_id
            }
        }), 200

    @staticmethod
    def delete_task(task_id):
        task = Task.query.get(task_id)
        if not task:
            return jsonify({'error': 'Task not found'}), 404

        db.session.delete(task)
        db.session.commit()

        return jsonify({'message': 'Task deleted successfully'}), 200
    
