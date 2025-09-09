from flask_restx import Api

api = Api(
    version="1.0",
    title="API de Gerenciamento de Tarefas",
    description="API para gerenciar usuários e tarefas",
    doc="/docs",
    mask_swagger=False,
)