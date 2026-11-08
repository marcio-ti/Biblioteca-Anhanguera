from app.services import emprestimos as servico


def emprestar(dados):
    return servico.emprestar(dados)


def devolver(emprestimo_id):
    return servico.devolver(emprestimo_id)


def listar_ativos():
    return servico.listar_ativos()


def listar_historico():
    return servico.listar_historico()
