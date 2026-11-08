// Solicita confirmação apenas nas ações de exclusão e devolução.
document.addEventListener('submit', (evento) => {
    const formulario = evento.target;
    const mensagem = formulario.dataset.confirmar;
    if (mensagem && !window.confirm(mensagem)) {
        evento.preventDefault();
    }
});
