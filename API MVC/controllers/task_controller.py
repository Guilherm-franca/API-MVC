from flask import render_template, redirect, request, url_for
from models.task import Task
from models.user import Usuario
from database import db


class TaskController:
    @staticmethod
    def list_tasks():
        tasks = Task.query.all()
        return render_template('tasks.html', tasks=tasks)
    
    @staticmethod
    def create_task():
        if request.method == 'GET':
            users = Usuario.query.all()
            return render_template('create_task.html', users=users)
        elif request.method == 'POST':
            title = request.form['title']
            description = request.form.get('description', '')
            user_id = request.form['user_id']
            new_task = Task(title=title, description=description, user_id=user_id)
            db.session.add(new_task)
            db.session.commit()
            return redirect(url_for('list_tasks'))
        
    @staticmethod
    def update_task_status(task_id):
        task = Task.query.get(task_id)
        if task:
            task.status = 'Concluído' if task.status == 'Pendente' else 'Pendente'
            db.session.commit()
        return redirect(url_for('list_tasks'))
    
    @staticmethod
    def delete_task(task_id):
        task = Task.query.get(task_id)
        if task:
            db.session.delete(task)
            db.session.commit()
        return redirect(url_for('list_tasks'))
