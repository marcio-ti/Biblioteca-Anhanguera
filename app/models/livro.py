from app.extensions import db


class Livro(db.Model):
    __tablename__ = 'livros'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    autor = db.Column(db.String(150), nullable=False)
    ano_publicacao = db.Column(db.Integer, nullable=False)
    total_copias = db.Column(db.Integer, nullable=False)
    copias_disponiveis = db.Column(db.Integer, nullable=False)

    emprestimos = db.relationship('Emprestimo', back_populates='livro')
