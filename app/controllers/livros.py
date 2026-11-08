from app.services import livros as servico


def cadastrar(dados):
    return servico.cadastrar(dados)


def editar(livro_id, dados):
    return servico.editar(livro_id, dados)


def excluir(livro_id):
    return servico.excluir(livro_id)


def obter(livro_id):
    return servico.obter(livro_id)


def consultar(filtros):
    return servico.consultar(filtros)


def listar_disponiveis():
    return servico.listar_disponiveis()
