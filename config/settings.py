import os
import secrets


class Config:
    # A chave pode ser informada em CHAVE_SECRETA. Para uso local, é criada na execução.
    SECRET_KEY = os.environ.get('CHAVE_SECRETA') or secrets.token_hex(32)
    SQLALCHEMY_DATABASE_URI = os.environ.get('BANCO_DADOS') or 'sqlite:///biblioteca.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROTECAO_CSRF = True
