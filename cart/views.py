from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

try:
    from products.models import Produto
except Exception:
    Produto = None

CART_SESSION_ID = 'cart'

def _get_cart(request):
    return request.session.get(CART_SESSION_ID, {})

def cart_detail(request):
    cart = _get_cart(request)
    items = []
    total = 0
    for pid, data in cart.items():
        if Produto:
            produto = get_object_or_404(Produto, pk=pid)
            qty = data.get('quantity', 0)
            subtotal = produto.preco * qty
            items.append({'produto': produto, 'quantity': qty, 'subtotal': subtotal})
            total += subtotal
    return render(request, 'cart/detail.html', {'items': items, 'total': total})

def add_to_cart(request, produto_id):
    produto = None
    if Produto:
        produto = get_object_or_404(Produto, pk=produto_id)
    cart = _get_cart(request)
    qty = int(request.POST.get('quantity', 1)) if request.method == 'POST' else 1
    item = cart.get(str(produto_id), {'quantity': 0})
    item['quantity'] = item.get('quantity', 0) + qty
    cart[str(produto_id)] = item
    request.session[CART_SESSION_ID] = cart

    # Resposta para requisição AJAX: retorna sucesso e quantidade adicionada
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # opcional: retornar nome do produto para animar popup
        return JsonResponse({'success': True, 'added': qty, 'produto_nome': produto.nome if produto else ''})

    return redirect('cart:detail')

def remove_from_cart(request, produto_id):
    cart = _get_cart(request)
    cart.pop(str(produto_id), None)
    request.session[CART_SESSION_ID] = cart
    return redirect('cart:detail')

@login_required
def checkout(request):
    # placeholder: aqui você chamará a criação do pedido (orders) e reduzirá estoque
    # por enquanto apenas limpa o carrinho e redireciona
    request.session.pop(CART_SESSION_ID, None)
    return redirect('orders:detail', order_id='00000000-0000-0000-0000-000000000000')
