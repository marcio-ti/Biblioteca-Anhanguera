import pytest

from app import create_app
from app.extensions import db
from app.models import Emprestimo, Livro, Usuario


@pytest.fixture
def aplicacao(tmp_path):
    app = create_app({
        'TESTING': True,
        'PROTECAO_CSRF': False,
        'SQLALCHEMY_DATABASE_URI': f'sqlite:///{tmp_path / "biblioteca_teste.db"}',
    })
    yield app
    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def cliente(aplicacao):
    return aplicacao.test_client()


def cadastrar_livro(cliente, titulo='Dom Casmurro', quantidade='2'):
    return cliente.post('/cadastrar_livro', data={
        'titulo': titulo,
        'autor': 'Machado de Assis',
        'ano_publicacao': '1899',
        'total_copias': quantidade,
    }, follow_redirects=True)


def cadastrar_usuario(cliente, identificacao='0001'):
    return cliente.post('/cadastrar_usuario', data={
        'nome': 'Maria Silva',
        'identificacao': identificacao,
        'contato': 'maria@exemplo.com',
    }, follow_redirects=True)


def teste_paginas_abrem(cliente):
    for caminho in ('/', '/cadastrar_livro', '/consultar_livro', '/cadastrar_usuario',
                    '/usuarios', '/emprestimo_livro', '/devolucao_livro', '/relatorio'):
        resposta = cliente.get(caminho)
        assert resposta.status_code == 200, caminho


def teste_cadastros_e_filtros(aplicacao, cliente):
    assert b'Livro cadastrado' in cadastrar_livro(cliente).data
    assert b'Usu\xc3\xa1rio cadastrado' in cadastrar_usuario(cliente).data
    assert b'Dom Casmurro' in cliente.get('/consultar_livro?titulo=dom').data
    assert b'Dom Casmurro' in cliente.get('/consultar_livro?autor=machado').data
    assert b'Dom Casmurro' in cliente.get('/consultar_livro?ano_publicacao=1899').data
    assert b'Nenhum livro encontrado' in cliente.get('/consultar_livro?ano_publicacao=2020').data
    assert b'ano de publica' in cliente.get('/consultar_livro?ano_publicacao=invalido').data
    assert b'Maria Silva' in cliente.get('/usuarios').data
    assert b'j\xc3\xa1 est\xc3\xa1 cadastrada' in cadastrar_usuario(cliente).data
    with aplicacao.app_context():
        assert db.session.query(Usuario).count() == 1
        assert db.session.query(Livro).count() == 1


def teste_emprestimo_devolucao_estoque_historico(aplicacao, cliente):
    cadastrar_livro(cliente, quantidade='1')
    cadastrar_usuario(cliente)
    resposta = cliente.post('/emprestimo_livro', data={'livro_id': '1', 'usuario_id': '1'}, follow_redirects=True)
    assert b'Empr\xc3\xa9stimo registrado' in resposta.data
    with aplicacao.app_context():
        assert db.session.get(Livro, 1).copias_disponiveis == 0
        assert db.session.get(Emprestimo, 1).situacao == 'emprestado'
    assert b'Dom Casmurro' in cliente.get('/devolucao_livro').data
    assert b'Dom Casmurro' not in cliente.get('/emprestimo_livro').data
    resposta = cliente.post('/emprestimo_livro', data={'livro_id': '1', 'usuario_id': '1'}, follow_redirects=True)
    assert b'n\xc3\xa3o possui c\xc3\xb3pias dispon\xc3\xadveis' in resposta.data
    assert b'Livros emprestados (1)' in cliente.get('/relatorio').data

    resposta = cliente.post('/devolucao_livro/1', follow_redirects=True)
    assert b'Devolu\xc3\xa7\xc3\xa3o registrada' in resposta.data
    with aplicacao.app_context():
        assert db.session.get(Livro, 1).copias_disponiveis == 1
        assert db.session.get(Emprestimo, 1).situacao == 'devolvido'
        assert db.session.get(Emprestimo, 1).data_devolucao is not None
    assert b'Hist\xc3\xb3rico de empr\xc3\xa9stimos (1)' in cliente.get('/relatorio').data
    assert b'Livros emprestados (0)' in cliente.get('/relatorio').data
    resposta = cliente.post('/devolucao_livro/1', follow_redirects=True)
    assert b'j\xc3\xa1 foi devolvido' in resposta.data
    with aplicacao.app_context():
        assert db.session.get(Livro, 1).copias_disponiveis == 1


def teste_validacoes_e_exclusao_segura(aplicacao, cliente):
    resposta = cadastrar_livro(cliente, quantidade='-1')
    assert b'maior ou igual a 0' in resposta.data
    cadastrar_livro(cliente, quantidade='2')
    cadastrar_usuario(cliente)
    resposta = cliente.post('/emprestimo_livro', data={'livro_id': '100', 'usuario_id': '1'}, follow_redirects=True)
    assert b'Livro n\xc3\xa3o encontrado' in resposta.data
    resposta = cliente.post('/emprestimo_livro', data={'livro_id': '1', 'usuario_id': '100'}, follow_redirects=True)
    assert b'Usu\xc3\xa1rio n\xc3\xa3o encontrado' in resposta.data
    cliente.post('/emprestimo_livro', data={'livro_id': '1', 'usuario_id': '1'})
    resposta = cliente.post('/alterar_livro/1', data={
        'titulo': 'Novo título', 'autor': 'Machado de Assis',
        'ano_publicacao': '1899', 'total_copias': '0',
    }, follow_redirects=True)
    assert b'total n\xc3\xa3o pode ser menor' in resposta.data
    assert b'n\xc3\xa3o \xc3\xa9 poss\xc3\xadvel excluir um livro' in cliente.post('/deletar_livro/1', follow_redirects=True).data.lower()
    assert b'n\xc3\xa3o \xc3\xa9 poss\xc3\xadvel excluir usu\xc3\xa1rio' in cliente.post('/deletar_usuario/1', follow_redirects=True).data.lower()
    with aplicacao.app_context():
        assert db.session.get(Livro, 1).total_copias == 2
        assert db.session.get(Livro, 1).copias_disponiveis == 1
        assert db.session.get(Usuario, 1) is not None


def teste_editar_e_excluir_sem_historico(aplicacao, cliente):
    cadastrar_livro(cliente)
    cadastrar_usuario(cliente)
    cliente.post('/alterar_livro/1', data={
        'titulo': 'Memórias Póstumas de Brás Cubas', 'autor': 'Machado de Assis',
        'ano_publicacao': '1881', 'total_copias': '5',
    })
    cliente.post('/alterar_usuario/1', data={
        'nome': 'Ana', 'identificacao': '0001', 'contato': 'ana@exemplo.com',
    })
    assert b'Mem\xc3\xb3rias P\xc3\xb3stumas' in cliente.get('/livro/1').data
    assert b'Ana' in cliente.get('/usuarios').data
    cliente.post('/deletar_livro/1')
    cliente.post('/deletar_usuario/1')
    with aplicacao.app_context():
        assert db.session.get(Livro, 1) is None
        assert db.session.get(Usuario, 1) is None


def teste_csrf_bloqueia_envio_sem_token(tmp_path):
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': f'sqlite:///{tmp_path / "csrf.db"}',
    })
    cliente = app.test_client()
    assert cliente.post('/cadastrar_livro', data={}).status_code == 400
    pagina = cliente.get('/cadastrar_livro')
    assert b'token_csrf' in pagina.data
    import re
    token = re.search(rb'name="token_csrf" value="([a-f0-9]+)"', pagina.data).group(1).decode()
    resposta = cliente.post('/cadastrar_livro', data={
        'token_csrf': token, 'titulo': 'Livro de teste', 'autor': 'Autor de teste',
        'ano_publicacao': '2001', 'total_copias': '1',
    }, follow_redirects=True)
    assert resposta.status_code == 200
    assert b'Livro de teste' in resposta.data
