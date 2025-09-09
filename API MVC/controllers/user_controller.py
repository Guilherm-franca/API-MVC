from flask import request, jsonify
from database import db
from models.user import Usuario

class UsuarioController:
    @staticmethod
    def criar_usuario():
        data = request.get_json()
        if not data:
            return jsonify({"error": "Request body must be JSON"}), 400

        if 'nome' not in data or 'email' not in data:
            return jsonify({"error": "Nome e email são obrigatórios"}), 400

        novo_usuario = Usuario(nome=data['nome'], email=data['email'])
        db.session.add(novo_usuario)
        db.session.commit()

        return jsonify(novo_usuario.to_dict()), 201

    @staticmethod
    def buscar_todos():
        usuarios = Usuario.query.all()
        return jsonify([u.to_dict() for u in usuarios]), 200

    @staticmethod
    def buscar_por_id(usuario_id):
        usuario = Usuario.query.get(usuario_id)
        if usuario is None:
            return jsonify({"error": "Usuário não encontrado"}), 404
        return jsonify(usuario.to_dict()), 200

    @staticmethod
    def atualizar(usuario_id):
        usuario = Usuario.query.get(usuario_id)
        if usuario is None:
            return jsonify({"error": "Usuário não encontrado"}), 404

        data = request.get_json()
        if not data:
            return jsonify({"error": "Request body must be JSON"}), 400

        if 'nome' in data:
            usuario.nome = data['nome']
        if 'email' in data:
            usuario.email = data['email']

        db.session.commit()
        return jsonify(usuario.to_dict()), 200

    @staticmethod
    def deletar(usuario_id):
        usuario = Usuario.query.get(usuario_id)
        if usuario is None:
            return jsonify({"error": "Usuário não encontrado"}), 404

        db.session.delete(usuario)
        db.session.commit()
        return jsonify({"message": "Usuário excluído com sucesso"}), 200
    