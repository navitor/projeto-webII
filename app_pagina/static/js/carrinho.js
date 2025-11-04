function carregarCarrinho() {
    const carrinho = JSON.parse(localStorage.getItem("carrinho")) || [];
    const lista = document.getElementById("lista-carrinho");
    const total = document.getElementById("total");

    lista.innerHTML = "";
    let soma = 0;

    if (carrinho.length === 0) {
        lista.innerHTML = "<p>Seu carrinho está vazio </p>";
        total.textContent = "";
        return;
    }

    carrinho.forEach((item, index) => {
        const precoNumerico = parseFloat(item.preco.replace("R$", "").replace(",", "."));
        soma += precoNumerico;

        const div = document.createElement("div");
        div.className = "item-carrinho";
        div.innerHTML = `
            <img src="${item.img}" alt="${item.nome}">
            <div>
                <h3>${item.nome}</h3>
                <p>${item.preco}</p>
                <button onclick="removerItem(${index})">❌ Remover</button>
            </div>
        `;
        lista.appendChild(div);
    });

    total.textContent = `Total: R$ ${soma.toFixed(2).replace(".", ",")}`;
    atualizarCarrinho();
}

function removerItem(index) {
    let carrinho = JSON.parse(localStorage.getItem("carrinho"));
    carrinho.splice(index, 1);
    localStorage.setItem("carrinho", JSON.stringify(carrinho));
    carregarCarrinho();
}

document.addEventListener("DOMContentLoaded", () => {
    carregarCarrinho();

    const finalizarBtn = document.getElementById("finalizar-compra");
    if (finalizarBtn) {
        finalizarBtn.addEventListener("click", () => {
            window.location.href = "{% url 'checkout' %}";
        });
    }
});