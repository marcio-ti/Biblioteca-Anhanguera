from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.controllers import emprestimos as controlador
from app.controllers import livros as controlador_livros
from app.controllers import usuarios as controlador_usuarios
from app.dto.dados import ErroBiblioteca

emprestimos_bp = Blueprint('emprestimos', __name__)


@emprestimos_bp.route('/emprestimo_livro', methods=['GET', 'POST'])
def emprestimo_livro():
    if request.method == 'POST':
        try:
            controlador.emprestar(request.form)
            flash('Empréstimo registrado com sucesso.', 'sucesso')
            return redirect(url_for('emprestimos.devolucao_livro'))
        except ErroBiblioteca as erro:
            flash(str(erro), 'erro')
    return render_template(
        'emprestimo_livro.html',
        livros=controlador_livros.listar_disponiveis(),
        usuarios=controlador_usuarios.listar(),
    )


@emprestimos_bp.route('/devolucao_livro')
def devolucao_livro():
    return render_template('devolucao_livro.html', emprestimos=controlador.listar_ativos())


@emprestimos_bp.route('/devolucao_livro/<int:emprestimo_id>', methods=['POST'])
def registrar_devolucao(emprestimo_id):
    try:
        controlador.devolver(emprestimo_id)
        flash('Devolução registrada com sucesso.', 'sucesso')
    except ErroBiblioteca as erro:
        flash(str(erro), 'erro')
    return redirect(url_for('emprestimos.devolucao_livro'))
