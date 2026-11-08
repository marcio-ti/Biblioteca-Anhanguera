from app.extensions import db


class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    identificacao = db.Column(db.String(60), unique=True, nullable=False)
    contato = db.Column(db.String(150), nullable=False)

    emprestimos = db.relationship('Emprestimo', back_populates='usuario')
