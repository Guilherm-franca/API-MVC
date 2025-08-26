from flask import Flask, request, jsonify
from database import db
from controllers.task_controller import TaskController
from controllers.user_controller import UsuarioController


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db.init_app(app)


with app.app_context():
    db.create_all()

@app.route('/usuarios', methods=['POST'])
def criar_usuario():
    return UsuarioController.criar_usuario()

@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    return UsuarioController.buscar_todos()

@app.route('/usuarios/<int:usuario_id>', methods=['GET'])
def buscar_usuario(usuario_id):
    return UsuarioController.buscar_por_id(usuario_id)

@app.route('/usuarios/<int:usuario_id>', methods=['PUT'])
def atualizar_usuario(usuario_id):
    return UsuarioController.atualizar(usuario_id)

@app.route('/usuarios/<int:usuario_id>', methods=['DELETE'])
def deletar_usuario(usuario_id):
    return UsuarioController.deletar(usuario_id)

@app.route('/tasks', methods=['GET'])
def list_tasks():
    return TaskController.list_tasks()

@app.route('/tasks/new', methods=['GET', 'POST'])
def create_task():
    return TaskController.create_task()

@app.route('/tasks/update/<int:task_id>', methods=['POST'])
def update_task_status(task_id):
    return TaskController.update_task_status(task_id)

@app.route('/tasks/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    return TaskController.delete_task(task_id)

if __name__ == '__main__':
    app.run(debug=True)
