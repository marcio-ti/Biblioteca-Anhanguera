from app.extensions import db
from app.models import Usuario


def buscar(usuario_id):
    return db.session.get(Usuario, usuario_id)


def por_identificacao(identificacao):
    consulta = db.select(Usuario).where(Usuario.identificacao == identificacao)
    return db.session.scalar(consulta)


def listar():
    return db.session.scalars(db.select(Usuario).order_by(Usuario.nome, Usuario.id)).all()


def salvar(usuario):
    db.session.add(usuario)
