from django.shortcuts import render, get_object_or_404

try:
    from .models import Produto
except Exception:
    Produto = None

def product_list(request):
    produtos = Produto.objects.all() if Produto else []
    return render(request, 'products/list.html', {'produtos': produtos})

def product_detail(request, pk):
    if not Produto:
        return render(request, 'products/detail.html', {'produto': None})
    produto = get_object_or_404(Produto, pk=pk)
    return render(request, 'products/detail.html', {'produto': produto})
