from sqlalchemy.exc import IntegrityError

from app.dto.dados import DadosUsuario, ErroBiblioteca
from app.extensions import db
from app.models import Usuario
from app.repositories import emprestimos as repositorio_emprestimos
from app.repositories import usuarios as repositorio_usuarios


def cadastrar(dados):
    dados = DadosUsuario.validar(dados)
    if repositorio_usuarios.por_identificacao(dados.identificacao):
        raise ErroBiblioteca('Esta identificação já está cadastrada.')
    usuario = Usuario(**vars(dados))
    repositorio_usuarios.salvar(usuario)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise ErroBiblioteca('Esta identificação já está cadastrada.') from None
    return usuario


def editar(usuario_id, dados):
    usuario = obter(usuario_id)
    dados = DadosUsuario.validar(dados)
    existente = repositorio_usuarios.por_identificacao(dados.identificacao)
    if existente and existente.id != usuario.id:
        raise ErroBiblioteca('Esta identificação já está cadastrada.')
    usuario.nome = dados.nome
    usuario.identificacao = dados.identificacao
    usuario.contato = dados.contato
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise ErroBiblioteca('Esta identificação já está cadastrada.') from None
    return usuario


def excluir(usuario_id):
    usuario = obter(usuario_id)
    if repositorio_emprestimos.existe_para_usuario(usuario_id):
        raise ErroBiblioteca('Não é possível excluir usuário com histórico de empréstimos.')
    db.session.delete(usuario)
    db.session.commit()


def obter(usuario_id):
    usuario = repositorio_usuarios.buscar(usuario_id)
    if usuario is None:
        raise ErroBiblioteca('Usuário não encontrado.')
    return usuario


def listar():
    return repositorio_usuarios.listar()
