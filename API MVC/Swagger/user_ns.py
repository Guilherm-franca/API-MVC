from flask_restx import Namespace, Resource, fields
from flask import request
from models.user import Usuario
from database import db

user_ns = Namespace('users', description='Operações relacionadas a usuários')

user_model = user_ns.model('User ', {
    'id': fields.Integer(readonly=True, example=1),
    'nome': fields.String(required=True, example='João Silva'),
    'email': fields.String(required=True, example='joao@example.com'),
})

user_create_model = user_ns.model('User Create', {
    'nome': fields.String(required=True, example='João Silva'),
    'email': fields.String(required=True, example='joao@example.com'),
})

@user_ns.route('')
class UserList(Resource):
    @user_ns.marshal_list_with(user_model)
    def get(self):
        """Listar todos os usuários"""
        users = Usuario.query.all()
        return users

    @user_ns.expect(user_create_model, validate=True)
    @user_ns.marshal_with(user_model, code=201)
    def post(self):
        """Criar um novo usuário"""
        data = request.json
        new_user = Usuario(nome=data['nome'], email=data['email'])
        db.session.add(new_user)
        db.session.commit()
        return new_user, 201

@user_ns.route('/<int:user_id>')
@user_ns.param('user_id', 'ID do usuário')
class User(Resource):
    @user_ns.marshal_with(user_model)
    def get(self, user_id):
        """Obter um usuário pelo ID"""
        user = Usuario.query.get_or_404(user_id, "Usuário não encontrado")
        return user

    @user_ns.expect(user_create_model, validate=True)
    @user_ns.marshal_with(user_model)
    def put(self, user_id):
        """Atualizar um usuário"""
        user = Usuario.query.get_or_404(user_id, "Usuário não encontrado")
        data = request.json

        user.nome = data['nome']
        user.email = data['email']

        db.session.commit()
        return user

    def delete(self, user_id):
        """Excluir um usuário"""
        user = Usuario.query.get_or_404(user_id, "Usuário não encontrado")
        db.session.delete(user)
        db.session.commit()
        return {'message': 'Usuário excluído com sucesso'}, 200