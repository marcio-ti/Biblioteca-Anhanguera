from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.controllers import emprestimos as controlador_emprestimos
from app.controllers import livros as controlador_livros
from app.controllers import usuarios as controlador_usuarios
from app.dto.dados import ErroBiblioteca

biblioteca_bp = Blueprint('biblioteca', __name__)


@biblioteca_bp.route('/')
def index():
    return render_template('index.html')


@biblioteca_bp.route('/cadastrar_livro', methods=['GET', 'POST'])
def cadastrar_livro():
    if request.method == 'POST':
        try:
            controlador_livros.cadastrar(request.form)
            flash('Livro cadastrado com sucesso.', 'sucesso')
            return redirect(url_for('biblioteca.consultar_livro'))
        except ErroBiblioteca as erro:
            flash(str(erro), 'erro')
    return render_template('formulario_livro.html', livro=None)


@biblioteca_bp.route('/consultar_livro')
def consultar_livro():
    try:
        livros = controlador_livros.consultar(request.args)
    except ErroBiblioteca as erro:
        flash(str(erro), 'erro')
        livros = []
    return render_template('consultar_livros.html', livros=livros)


@biblioteca_bp.route('/livro/<int:livro_id>')
def detalhe_livro(livro_id):
    try:
        livro = controlador_livros.obter(livro_id)
    except ErroBiblioteca as erro:
        flash(str(erro), 'erro')
        return redirect(url_for('biblioteca.consultar_livro'))
    return render_template('detalhe_livro.html', livro=livro)


@biblioteca_bp.route('/alterar_livro/<int:livro_id>', methods=['GET', 'POST'])
def alterar_livro(livro_id):
    try:
        livro = controlador_livros.obter(livro_id)
    except ErroBiblioteca as erro:
        flash(str(erro), 'erro')
        return redirect(url_for('biblioteca.consultar_livro'))

    if request.method == 'POST':
        try:
            controlador_livros.editar(livro_id, request.form)
            flash('Livro atualizado com sucesso.', 'sucesso')
            return redirect(url_for('biblioteca.consultar_livro'))
        except ErroBiblioteca as erro:
            flash(str(erro), 'erro')
    return render_template('formulario_livro.html', livro=livro)


@biblioteca_bp.route('/deletar_livro/<int:livro_id>', methods=['POST'])
def deletar_livro(livro_id):
    try:
        controlador_livros.excluir(livro_id)
        flash('Livro excluído com sucesso.', 'sucesso')
    except ErroBiblioteca as erro:
        flash(str(erro), 'erro')
    return redirect(url_for('biblioteca.consultar_livro'))


@biblioteca_bp.route('/relatorio')
def relatorio():
    return render_template(
        'relatorio.html',
        livros=controlador_livros.listar_disponiveis(),
        emprestimos=controlador_emprestimos.listar_ativos(),
        usuarios=controlador_usuarios.listar(),
        historico=controlador_emprestimos.listar_historico(),
    )
