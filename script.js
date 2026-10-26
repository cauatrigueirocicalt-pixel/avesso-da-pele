// Espera todo o HTML da página ser carregado.
document.addEventListener("DOMContentLoaded", () => {
    configurarMenu();
    configurarBusca();
    configurarParticipacao();
    configurarBotaoTopo();
});


// ======================================================
// MENU PARA CELULARES
// ======================================================

function configurarMenu() {
    const botaoMenu = document.querySelector(".botao-menu");
    const menu = document.querySelector("#menu-principal");

    // Evita erros nas páginas que não possuem esses elementos.
    if (!botaoMenu || !menu) {
        return;
    }

    botaoMenu.addEventListener("click", () => {
        const menuEstaAberto = menu.classList.toggle("aberto");

        // Informa aos leitores de tela se o menu está aberto.
        botaoMenu.setAttribute(
            "aria-expanded",
            String(menuEstaAberto)
        );

        // Altera o texto do botão.
        botaoMenu.textContent = menuEstaAberto
            ? "Fechar"
            : "Menu";
    });
}


// ======================================================
// VALIDAÇÃO DA PESQUISA
// ======================================================

function configurarBusca() {
    const formularios = document.querySelectorAll(
        "[data-validar-busca]"
    );

    formularios.forEach((formulario) => {
        formulario.addEventListener("submit", (evento) => {
            const campo = formulario.querySelector(
                "input[name='termo']"
            );

            if (!campo) {
                return;
            }

            // trim() retira espaços antes e depois do texto.
            const termo = campo.value.trim();

            if (termo.length < 2) {
                evento.preventDefault();

                alert(
                    "Digite pelo menos dois caracteres para pesquisar."
                );

                campo.focus();
                return;
            }

            // Envia o termo já sem os espaços desnecessários.
            campo.value = termo;
        });
    });
}


// ======================================================
// CONFIRMAÇÃO DA PARTICIPAÇÃO
// ======================================================

function configurarParticipacao() {
    const formulario = document.querySelector(
        "[data-confirmar-participacao]"
    );

    if (!formulario) {
        return;
    }

    formulario.addEventListener("submit", (evento) => {
        const opcao = formulario.querySelector(
            "input[name='palavra']:checked"
        );

        // Impede o envio se nenhuma palavra foi selecionada.
        if (!opcao) {
            evento.preventDefault();

            alert(
                "Escolha uma palavra antes de continuar."
            );

            return;
        }

        const confirmar = confirm(
            `Você escolheu “${opcao.value}”. ` +
            "Deseja registrar essa participação?"
        );

        // Cancela o envio se o usuário escolher “Cancelar”.
        if (!confirmar) {
            evento.preventDefault();
        }
    });
}


// ======================================================
// BOTÃO VOLTAR AO TOPO
// ======================================================

function configurarBotaoTopo() {
    const botaoTopo = document.querySelector("#voltar-topo");

    if (!botaoTopo) {
        return;
    }

    window.addEventListener("scroll", () => {
        const deveAparecer = window.scrollY > 400;

        botaoTopo.classList.toggle(
            "visivel",
            deveAparecer
        );
    });

    botaoTopo.addEventListener("click", () => {
        window.scrollTo({
            top: 0,
            behavior: "smooth"
        });
    });
}