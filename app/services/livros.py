from app.dto.dados import DadosLivro, ErroBiblioteca
from app.extensions import db
from app.models import Livro
from app.repositories import emprestimos as repositorio_emprestimos
from app.repositories import livros as repositorio_livros


def cadastrar(dados):
    dados = DadosLivro.validar(dados)
    livro = Livro(
        titulo=dados.titulo,
        autor=dados.autor,
        ano_publicacao=dados.ano_publicacao,
        total_copias=dados.total_copias,
        copias_disponiveis=dados.total_copias,
    )
    repositorio_livros.salvar(livro)
    db.session.commit()
    return livro


def editar(livro_id, dados):
    livro = obter(livro_id)
    dados = DadosLivro.validar(dados)
    emprestadas = livro.total_copias - livro.copias_disponiveis
    if dados.total_copias < emprestadas:
        raise ErroBiblioteca('O total não pode ser menor que as cópias emprestadas.')
    livro.titulo = dados.titulo
    livro.autor = dados.autor
    livro.ano_publicacao = dados.ano_publicacao
    livro.total_copias = dados.total_copias
    livro.copias_disponiveis = dados.total_copias - emprestadas
    db.session.commit()
    return livro


def excluir(livro_id):
    livro = obter(livro_id)
    if repositorio_emprestimos.existe_para_livro(livro_id):
        raise ErroBiblioteca('Não é possível excluir um livro com histórico de empréstimos.')
    db.session.delete(livro)
    db.session.commit()


def obter(livro_id):
    livro = repositorio_livros.buscar(livro_id)
    if livro is None:
        raise ErroBiblioteca('Livro não encontrado.')
    return livro


def consultar(filtros):
    titulo = str(filtros.get('titulo', '')).strip()
    autor = str(filtros.get('autor', '')).strip()
    ano_texto = str(filtros.get('ano_publicacao', '')).strip()
    ano = None
    if ano_texto:
        try:
            ano = int(ano_texto)
        except ValueError:
            raise ErroBiblioteca('Informe um ano de publicação válido.') from None
        if ano < 1:
            raise ErroBiblioteca('Informe um ano de publicação válido.')
    return repositorio_livros.listar(titulo=titulo, autor=autor, ano=ano)


def listar_disponiveis():
    return repositorio_livros.disponiveis()
