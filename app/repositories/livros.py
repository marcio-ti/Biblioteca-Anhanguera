from app.extensions import db
from app.models import Livro


def buscar(livro_id):
    return db.session.get(Livro, livro_id)


def listar(titulo='', autor='', ano=None):
    consulta = db.select(Livro)
    if titulo:
        consulta = consulta.where(Livro.titulo.ilike(f'%{titulo}%'))
    if autor:
        consulta = consulta.where(Livro.autor.ilike(f'%{autor}%'))
    if ano is not None:
        consulta = consulta.where(Livro.ano_publicacao == ano)
    return db.session.scalars(consulta.order_by(Livro.titulo, Livro.id)).all()


def disponiveis():
    consulta = db.select(Livro).where(Livro.copias_disponiveis > 0).order_by(Livro.titulo)
    return db.session.scalars(consulta).all()


def salvar(livro):
    db.session.add(livro)
