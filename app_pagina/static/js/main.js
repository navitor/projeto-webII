if (!localStorage.getItem("carrinho")) {
    localStorage.setItem("carrinho", JSON.stringify([]));
}

// Atualiza o contador no header
function atualizarCarrinho() {
    const carrinho = JSON.parse(localStorage.getItem("carrinho"));
    const contador = document.getElementById("carrinho-contador");
    if (contador) {
        contador.textContent = carrinho.length;
    }
}

// Adiciona produto ao carrinho
function adicionarCarrinho(produto) {
    let carrinho = JSON.parse(localStorage.getItem("carrinho"));
    carrinho.push(produto);
    localStorage.setItem("carrinho", JSON.stringify(carrinho));
    atualizarCarrinho();
    mostrarToast(`✅ ${produto.nome} adicionado ao carrinho!`);
}

// Exibe notificação 
function mostrarToast(msg) {
    const toast = document.createElement("div");
    toast.className = "toast";
    toast.textContent = msg;
    document.body.appendChild(toast);

    setTimeout(() => {
        toast.classList.add("show");
    }, 100);

    setTimeout(() => {
        toast.classList.remove("show");
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

//Inicialização ao carregar a página
document.addEventListener("DOMContentLoaded", () => {
    atualizarCarrinho();

    // Captura todos os botões que devem adicionar ao carrinho
    const botoesAdicionar = document.querySelectorAll(".btn-comprar");
    botoesAdicionar.forEach((btn) => {
        btn.addEventListener("click", (e) => {
            const produtoId = e.target.getAttribute("data-produto-id");
            if (produtoId) {
                const produtoSimulado = {
                    id: produtoId,
                    nome: "Pijama Simulado", 
                    preco: 99.90, 
                    imagem: "/media/pijama.jpeg"
                };
                adicionarCarrinho(produtoSimulado);
            }
        });
    });


const toggleBtn = document.querySelector(".menu-toggle");
const navMenu = document.querySelector(".nav-menu");

if (toggleBtn && navMenu) {
    toggleBtn.addEventListener("click", () => {
        navMenu.classList.toggle("show");
        toggleBtn.classList.toggle("active"); 
    });
}

});

const slides = document.querySelectorAll(".slide");
let currentSlide = 0;

function showSlide(index) {
    slides.forEach((slide, i) => {
        slide.classList.remove("active");
        if (i === index) slide.classList.add("active");
    });
}

document.querySelector(".next").addEventListener("click", () => {
    currentSlide = (currentSlide + 1) % slides.length;
    showSlide(currentSlide);
});

document.querySelector(".prev").addEventListener("click", () => {
    currentSlide = (currentSlide - 1 + slides.length) % slides.length;
    showSlide(currentSlide);
});

// troca automática a cada 5s
setInterval(() => {
    currentSlide = (currentSlide + 1) % slides.length;
    showSlide(currentSlide);
}, 5000);
