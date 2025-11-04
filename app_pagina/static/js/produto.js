document.addEventListener("DOMContentLoaded", () => {

    const btnAdicionarCarrinho = document.querySelector(".btn-comprar");

    // Adiciona um listener no botão de comprar
    if (btnAdicionarCarrinho) {
        btnAdicionarCarrinho.addEventListener("click", () => {

            // Coleta o ID do produto do atributo de dados do botão
            const produtoId = btnAdicionarCarrinho.getAttribute("data-produto-id");
            if (!produtoId) {
                console.error("ID do produto não encontrado.");
                return;
            }

            // Coleta os dados dinâmicos da página (gerados pelo Django)
            const produto = {
                id: produtoId,
                nome: document.querySelector(".produto-info h1").textContent,
                preco: parseFloat(document.querySelector(".produto-info .preco").textContent.replace("R$ ", "").replace(",", ".")),
                // Adicione a imagem aqui se houver um elemento para ela na página
                tamanho: document.getElementById("tamanho") ? document.getElementById("tamanho").value : null,
                cor: document.getElementById("cor") ? document.getElementById("cor").value : null,
                personalizacao: document.getElementById("personalizacao") ? document.getElementById("personalizacao").value : null,
            };

            // Pega o carrinho existente ou cria um novo
            let carrinho = JSON.parse(localStorage.getItem("carrinho")) || [];
            carrinho.push(produto);
            localStorage.setItem("carrinho", JSON.stringify(carrinho));

            // Notifica o usuário 
            if (typeof mostrarToast !== 'undefined') {
                mostrarToast(`✅ ${produto.nome} adicionado ao carrinho!`);
            } else {
                alert(`✅ ${produto.nome} adicionado ao carrinho!`);
            }
        });
    }
});