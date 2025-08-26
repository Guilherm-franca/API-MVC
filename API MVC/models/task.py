from database import db

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    status = db.Column(db.String, nullable=False, default='Pendente')
    user_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

    user = db.relationship("Usuario", back_populates="tasks")
