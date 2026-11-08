from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.controllers import usuarios as controlador
from app.dto.dados import ErroBiblioteca

usuarios_bp = Blueprint('usuarios', __name__)


@usuarios_bp.route('/cadastrar_usuario', methods=['GET', 'POST'])
def cadastrar_usuario():
    if request.method == 'POST':
        try:
            controlador.cadastrar(request.form)
            flash('Usuário cadastrado com sucesso.', 'sucesso')
            return redirect(url_for('usuarios.consultar_usuarios'))
        except ErroBiblioteca as erro:
            flash(str(erro), 'erro')
    return render_template('formulario_usuario.html', usuario=None)


@usuarios_bp.route('/usuarios')
def consultar_usuarios():
    return render_template('consultar_usuarios.html', usuarios=controlador.listar())


@usuarios_bp.route('/alterar_usuario/<int:usuario_id>', methods=['GET', 'POST'])
def alterar_usuario(usuario_id):
    try:
        usuario = controlador.obter(usuario_id)
    except ErroBiblioteca as erro:
        flash(str(erro), 'erro')
        return redirect(url_for('usuarios.consultar_usuarios'))

    if request.method == 'POST':
        try:
            controlador.editar(usuario_id, request.form)
            flash('Usuário atualizado com sucesso.', 'sucesso')
            return redirect(url_for('usuarios.consultar_usuarios'))
        except ErroBiblioteca as erro:
            flash(str(erro), 'erro')
    return render_template('formulario_usuario.html', usuario=usuario)


@usuarios_bp.route('/deletar_usuario/<int:usuario_id>', methods=['POST'])
def deletar_usuario(usuario_id):
    try:
        controlador.excluir(usuario_id)
        flash('Usuário excluído com sucesso.', 'sucesso')
    except ErroBiblioteca as erro:
        flash(str(erro), 'erro')
    return redirect(url_for('usuarios.consultar_usuarios'))
