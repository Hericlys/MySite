const headerMenu = document.querySelector('[data-header="menu"]')

function AnimateMenuScroll() {
    const windowTop = window.pageYOffset;
    if (windowTop > 0) {
        headerMenu.classList.add('menu-shadow')
    }
    else {
        headerMenu.classList.remove('menu-shadow')
    }
}

window.addEventListener('scroll', function() {
    AnimateMenuScroll();
})

// Notification

document.addEventListener('DOMContentLoaded', function() {
    const sysMessage = document.querySelector('.sys-message');
    const messages = document.querySelectorAll('.sys-message .message');
    const displayTime = 10000; // Tempo de exibição das mensagens em milissegundos
    const fadeTime = 1000; // Tempo de transição de opacidade em milissegundos

    messages.forEach((message, index) => {
        setTimeout(() => {
            message.style.opacity = '0';
            message.style.transition = `opacity ${fadeTime / 1000}s ease`;

            setTimeout(() => {
                message.remove();

                if (document.querySelectorAll('.sys-message .message').length === 0) {
                    sysMessage.style.opacity = '0';
                    sysMessage.style.transition = `opacity ${fadeTime / 1000}s ease`;

                    setTimeout(() => {
                        sysMessage.remove();
                    }, fadeTime);
                }
            }, fadeTime);
        }, displayTime + (index * 1000)); // Atraso de 1 segundo adicional por mensagem
    });
});