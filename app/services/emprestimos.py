from datetime import datetime, timezone

from sqlalchemy import update

from app.dto.dados import ErroBiblioteca
from app.extensions import db
from app.models import Emprestimo, Livro
from app.repositories import emprestimos as repositorio_emprestimos
from app.repositories import livros as repositorio_livros
from app.repositories import usuarios as repositorio_usuarios


def _identificador(valor):
    try:
        identificador = int(str(valor).strip())
    except (ValueError, TypeError):
        raise ErroBiblioteca('Selecione um livro e um usuário válidos.') from None
    if identificador < 1:
        raise ErroBiblioteca('Selecione um livro e um usuário válidos.')
    return identificador


def emprestar(dados):
    livro_id = _identificador(dados.get('livro_id'))
    usuario_id = _identificador(dados.get('usuario_id'))
    if repositorio_livros.buscar(livro_id) is None:
        raise ErroBiblioteca('Livro não encontrado.')
    if repositorio_usuarios.buscar(usuario_id) is None:
        raise ErroBiblioteca('Usuário não encontrado.')

    # O UPDATE só retira uma cópia se ainda existir disponibilidade.
    resultado = db.session.execute(
        update(Livro)
        .where(Livro.id == livro_id, Livro.copias_disponiveis > 0)
        .values(copias_disponiveis=Livro.copias_disponiveis - 1)
    )
    if resultado.rowcount != 1:
        db.session.rollback()
        raise ErroBiblioteca('Este livro não possui cópias disponíveis.')

    emprestimo = Emprestimo(livro_id=livro_id, usuario_id=usuario_id, situacao='emprestado')
    repositorio_emprestimos.salvar(emprestimo)
    db.session.commit()
    return emprestimo


def devolver(emprestimo_id):
    emprestimo = repositorio_emprestimos.buscar(emprestimo_id)
    if emprestimo is None:
        raise ErroBiblioteca('Empréstimo não encontrado.')

    # A condição impede que a mesma devolução seja registrada duas vezes.
    resultado = db.session.execute(
        update(Emprestimo)
        .where(Emprestimo.id == emprestimo_id, Emprestimo.situacao == 'emprestado')
        .values(situacao='devolvido', data_devolucao=datetime.now(timezone.utc))
    )
    if resultado.rowcount != 1:
        db.session.rollback()
        raise ErroBiblioteca('Este empréstimo já foi devolvido.')
    db.session.execute(
        update(Livro)
        .where(Livro.id == emprestimo.livro_id)
        .values(copias_disponiveis=Livro.copias_disponiveis + 1)
    )
    db.session.commit()


def listar_ativos():
    return repositorio_emprestimos.listar(ativos_apenas=True)


def listar_historico():
    return repositorio_emprestimos.listar()
