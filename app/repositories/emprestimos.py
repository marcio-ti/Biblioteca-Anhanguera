from sqlalchemy.orm import joinedload

from app.extensions import db
from app.models import Emprestimo


def buscar(emprestimo_id):
    return db.session.get(Emprestimo, emprestimo_id)


def listar(ativos_apenas=False):
    consulta = db.select(Emprestimo).options(
        joinedload(Emprestimo.livro), joinedload(Emprestimo.usuario)
    )
    if ativos_apenas:
        consulta = consulta.where(Emprestimo.situacao == 'emprestado')
    consulta = consulta.order_by(Emprestimo.data_emprestimo.desc(), Emprestimo.id.desc())
    return db.session.scalars(consulta).all()


def existe_para_livro(livro_id):
    return db.session.scalar(
        db.select(Emprestimo.id).where(Emprestimo.livro_id == livro_id).limit(1)
    ) is not None


def existe_para_usuario(usuario_id):
    return db.session.scalar(
        db.select(Emprestimo.id).where(Emprestimo.usuario_id == usuario_id).limit(1)
    ) is not None


def salvar(emprestimo):
    db.session.add(emprestimo)
