from django.shortcuts import render, get_object_or_404, redirect
from .models import Produto, Categoria, Pedido, ItemPedido, Pagamento,UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Home 
def index(request):
    destaques = Produto.objects.all()[:4]  
    return render(request, "app_pagina/index.html", {"destaques": destaques})

# Listagem de Produtos
def produtos(request):
    lista_produtos = Produto.objects.all()
    return render(request, "app_pagina/produtos.html", {"produtos": lista_produtos})

# Detalhe do Produto
def produto_detalhe(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    return render(request, "app_pagina/produto_detalhe.html", {"produto": produto})

# Carrinho (sessão)
def adicionar_carrinho(request, produto_id):
    carrinho = request.session.get("carrinho", {})

    if str(produto_id) in carrinho:
        carrinho[str(produto_id)]["quantidade"] += 1
    else:
        produto = get_object_or_404(Produto, id=produto_id)
        carrinho[str(produto_id)] = {
            "nome": produto.nome,
            "preco": float(produto.preco),
            "quantidade": 1,
            "imagem": produto.imagem.url if produto.imagem else "",
        }

    request.session["carrinho"] = carrinho
    request.session.modified = True
    return redirect("carrinho")


def remover_carrinho(request, produto_id):
    carrinho = request.session.get("carrinho", {})

    if str(produto_id) in carrinho:
        del carrinho[str(produto_id)]
        request.session["carrinho"] = carrinho
        request.session.modified = True

    return redirect("carrinho")


def carrinho(request):
    carrinho = request.session.get("carrinho", {})
    total = sum(item["preco"] * item["quantidade"] for item in carrinho.values())
    return render(request, "app_pagina/carrinho.html", {"carrinho": carrinho, "total": total})

# Checkout & Pedido
def checkout(request):
    return render(request, "app_pagina/checkout.html")


def confirmacao(request):
    return render(request, "app_pagina/confirmacao_pedido.html")

# Páginas Institucionais
def sobre(request):
    return render(request, "app_pagina/sobre_nos.html")

def contato(request):
    return render(request, "app_pagina/contato.html")

def politicas(request):
    return render(request, "app_pagina/politicas.html")

# Autenticação (básico)
def login_usuario(request):
    return render(request, "app_pagina/login.html")

def criar_conta(request):
    if request.method == "POST":
        nome = request.POST["nome"]
        email = request.POST["email"]
        senha = request.POST["senha"]
        confirmar_senha = request.POST["confirmar_senha"]

        telefone = request.POST.get("telefone")
        endereco = request.POST.get("endereco")
        cidade = request.POST.get("cidade")
        estado = request.POST.get("estado")

        if senha != confirmar_senha:
            messages.error(request, "As senhas não coincidem.")
            return redirect("criar_conta")

        if User.objects.filter(username=email).exists():
            messages.error(request, "Já existe uma conta com este e-mail.")
            return redirect("criar_conta")

        # Criar usuário
        usuario = User.objects.create_user(
            username=email,
            email=email,
            password=senha,
            first_name=nome
        )

        # Criar perfil do usuário
        UserProfile.objects.create(
            usuario=usuario,
            telefone=telefone,
            endereco=endereco,
            cidade=cidade,
            estado=estado
        )

        # Login automático após cadastro
        login(request, usuario)
        messages.success(request, "Conta criada com sucesso! Bem-vindo(a) 💖")
        return redirect("index")

    return render(request, "app_pagina/criar_conta.html")


def recuperar_senha(request):
    return render(request, "app_pagina/recuperar_senha.html")

def logout_usuario(request):
    return redirect("index")

# Área do Cliente
def minha_conta(request):
    return render(request, "app_pagina/minha_conta.html")

def meus_dados(request):
    return render(request, "app_pagina/meus_dados.html")

def meus_pedidos(request):
    return render(request, "app_pagina/meus_pedidos.html")

def rastrear_pedido(request):
    return render(request, "app_pagina/rastrear_pedido.html")

@login_required
def pedido_detalhe(request, pedido_id):
    """
    Mostra os detalhes de um pedido específico do usuário logado.
    """
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)
    itens = pedido.itens.all()  

    return render(
        request,
        "app_pagina/pedido_detalhe.html",
        {"pedido": pedido, "itens": itens}
    )

def login_usuario(request):
    if request.method == "POST":
        email = request.POST["email"]
        senha = request.POST["senha"]

        usuario = authenticate(request, username=email, password=senha)

        if usuario is not None:
            login(request, usuario)
            messages.success(request, "Login realizado com sucesso!")
            return redirect("index")
        else:
            messages.error(request, "E-mail ou senha inválidos.")
            return redirect("login")

    return render(request, "app_pagina/login.html")

def logout_usuario(request):
    logout(request)
    messages.info(request, "Você saiu da sua conta.")
    return redirect("index")

def recuperar_senha(request):
    if request.method == "POST":
        email = request.POST["email"]
        if User.objects.filter(email=email).exists():
            messages.success(request, "Se este e-mail existir, enviaremos instruções para redefinir a senha.")
        else:
            messages.error(request, "E-mail não encontrado.")
        return redirect("recuperar_senha")

    return render(request, "app_pagina/recuperar_senha.html")
