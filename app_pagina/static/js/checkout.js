// CSRF Token gerado pelo Django
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

// formulário de checkout
const form = document.getElementById('checkout-form');

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    console.log('Formulário enviado');

    //Coleta os dados do cliente do formulário
    const infoCliente = {
        nome: form.querySelector('[name=nome]').value,
        email: form.querySelector('[name=email]').value,
        endereco: form.querySelector('[name=endereco]').value,
        cidade: form.querySelector('[name=cidade]').value,
        estado: form.querySelector('[name=estado]').value,
        cep: form.querySelector('[name=cep]').value,
    };

    // Coleta os itens do carrinho do localStorage
    const carrinhoItems = JSON.parse(localStorage.getItem('carrinho') || '[]');

    //Monta o objeto de dados para enviar ao back-end
    const dadosEnvio = {
        info_cliente: infoCliente,
        carrinho_items: carrinhoItems,
    };

    //Envia os dados para a view de checkout do Django
    try {
        const response = await fetch('/checkout/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify(dadosEnvio),
        });

        const data = await response.json();

        if (response.ok) {
            console.log('Pedido processado com sucesso!', data);
            localStorage.removeItem('carrinho');
            window.location.href = '/confirmacao/';
        } else {
            console.error('Erro ao processar o pedido:', data.error);
            alert('Erro ao processar o pedido. Tente novamente.');
        }
    } catch (error) {
        console.error('Erro na requisição:', error);
        alert('Erro de conexão. Verifique sua rede.');
    }
});