from app.services import usuarios as servico


def cadastrar(dados):
    return servico.cadastrar(dados)


def editar(usuario_id, dados):
    return servico.editar(usuario_id, dados)


def excluir(usuario_id):
    return servico.excluir(usuario_id)


def obter(usuario_id):
    return servico.obter(usuario_id)


def listar():
    return servico.listar()
