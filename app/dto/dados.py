from dataclasses import dataclass


class ErroBiblioteca(ValueError):
    """Erro esperado de validação ou de regra da biblioteca."""


def texto_obrigatorio(dados, campo, limite, descricao):
    valor = str(dados.get(campo, '')).strip()
    if not valor:
        raise ErroBiblioteca(f'Informe {descricao}.')
    if len(valor) > limite:
        raise ErroBiblioteca(f'{descricao.capitalize()} deve ter no máximo {limite} caracteres.')
    return valor


def numero_inteiro(dados, campo, descricao, minimo=0):
    try:
        valor = int(str(dados.get(campo, '')).strip())
    except (ValueError, TypeError):
        raise ErroBiblioteca(f'Informe {descricao} válido.') from None
    if valor < minimo:
        raise ErroBiblioteca(f'{descricao.capitalize()} deve ser maior ou igual a {minimo}.')
    return valor


@dataclass
class DadosLivro:
    titulo: str
    autor: str
    ano_publicacao: int
    total_copias: int

    @classmethod
    def validar(cls, dados):
        return cls(
            titulo=texto_obrigatorio(dados, 'titulo', 200, 'o título'),
            autor=texto_obrigatorio(dados, 'autor', 150, 'o autor'),
            ano_publicacao=numero_inteiro(dados, 'ano_publicacao', 'o ano de publicação', 1),
            total_copias=numero_inteiro(dados, 'total_copias', 'o número de cópias', 0),
        )


@dataclass
class DadosUsuario:
    nome: str
    identificacao: str
    contato: str

    @classmethod
    def validar(cls, dados):
        return cls(
            nome=texto_obrigatorio(dados, 'nome', 150, 'o nome'),
            identificacao=texto_obrigatorio(dados, 'identificacao', 60, 'a identificação'),
            contato=texto_obrigatorio(dados, 'contato', 150, 'o contato'),
        )
