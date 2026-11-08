import hmac
import os
import secrets

from flask import Flask, abort, request, session

from app.extensions import db
from config.settings import Config


def create_app(configuracoes=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    if configuracoes:
        app.config.update(configuracoes)

    os.makedirs(app.instance_path, exist_ok=True)
    db.init_app(app)

    from app.models import Emprestimo, Livro, Usuario  # Registra as tabelas.
    from app.views.livros import biblioteca_bp
    from app.views.usuarios import usuarios_bp
    from app.views.emprestimos import emprestimos_bp

    app.register_blueprint(biblioteca_bp)
    app.register_blueprint(usuarios_bp)
    app.register_blueprint(emprestimos_bp)

    @app.context_processor
    def fornecer_token():
        def token_csrf():
            if 'token_csrf' not in session:
                session['token_csrf'] = secrets.token_hex(32)
            return session['token_csrf']
        return {'token_csrf': token_csrf}

    @app.before_request
    def verificar_formulario():
        if request.method == 'POST' and app.config['PROTECAO_CSRF']:
            recebido = request.form.get('token_csrf', '')
            esperado = session.get('token_csrf', '')
            if not recebido or not hmac.compare_digest(recebido, esperado):
                abort(400, description='Formulário inválido. Atualize a página e tente novamente.')

    # Criação simples da base local, sem exigir comandos manuais de migração.
    with app.app_context():
        db.create_all()

    return app
