document.addEventListener('DOMContentLoaded', function () {
  const cartBadge = document.getElementById('cart-badge');
  const cartPopup = document.getElementById('cart-popup');

  // Função para animar popup
  function showPopup(text) {
    if (!cartPopup) return;
    cartPopup.textContent = text || '+1';
    cartPopup.classList.add('visible');
    setTimeout(() => cartPopup.classList.remove('visible'), 900);
  }

  // Atualiza badge com total de itens (soma simples)
  function updateBadge(delta) {
    if (!cartBadge) return;
    const cur = parseInt(cartBadge.textContent || '0', 10);
    cartBadge.textContent = Math.max(0, cur + (delta || 0));
  }

  // Captura todos os formulários/buttons que adicionam ao carrinho
  // Recomendado: botões/formulários com classe .add-to-cart
  document.querySelectorAll('.add-to-cart').forEach(function (el) {
    el.addEventListener('click', function (e) {
      e.preventDefault();
      // suporta <form class="add-to-cart"> ou <a data-url class="add-to-cart">
      let form = el.tagName.toLowerCase() === 'form' ? el : el.closest('form');
      let url = null;
      let body = null;
      if (form) {
        url = form.getAttribute('action') || window.location.href;
        body = new FormData(form);
      } else {
        url = el.getAttribute('data-url');
        body = new FormData();
      }

      fetch(url, {
        method: 'POST',
        headers: {
          'X-Requested-With': 'XMLHttpRequest',
          'X-CSRFToken': getCookie('csrftoken'),
        },
        body: body
      })
      .then(resp => resp.json())
      .then(data => {
        if (data && data.success) {
          showPopup('+' + (data.added || 1));
          updateBadge(data.added || 1);
        } else {
          // fallback: recarregar página se não for JSON
          window.location.reload();
        }
      })
      .catch(() => window.location.reload());
    });
  });

  // helper para pegar csrf token
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
});