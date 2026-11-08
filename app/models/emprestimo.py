from datetime import datetime, timezone

from app.extensions import db


def data_atual():
    return datetime.now(timezone.utc)


class Emprestimo(db.Model):
    __tablename__ = 'emprestimos'

    id = db.Column(db.Integer, primary_key=True)
    livro_id = db.Column(db.Integer, db.ForeignKey('livros.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    data_emprestimo = db.Column(db.DateTime(timezone=True), nullable=False, default=data_atual)
    data_devolucao = db.Column(db.DateTime(timezone=True), nullable=True)
    situacao = db.Column(db.String(20), nullable=False, default='emprestado')

    livro = db.relationship('Livro', back_populates='emprestimos')
    usuario = db.relationship('Usuario', back_populates='emprestimos')
