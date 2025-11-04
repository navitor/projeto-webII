from django.urls import path
from . import views

urlpatterns = [
    # Páginas da Loja
    path('', views.index, name='index'),
    path('produtos/', views.produtos, name='produtos'),
    path('produto/<int:pk>/', views.produto_detalhe, name='produto_detalhe'),
    path('carrinho/', views.carrinho, name='carrinho'),
    path('checkout/', views.checkout, name='checkout'),
    path('confirmacao/', views.confirmacao, name='confirmacao_pedido'),

    # Páginas Institucionais
    path('sobre-nos/', views.sobre, name='sobre_nos'),
    path('contato/', views.contato, name='contato'),
    path('politicas/', views.politicas, name='politicas'),

    # Páginas de Autenticação
    path('login/', views.login_usuario, name='login'),
    path('criar-conta/', views.criar_conta, name='criar_conta'),
    path('recuperar-senha/', views.recuperar_senha, name='recuperar_senha'),
    path('logout/', views.logout_usuario, name='logout'),

    # Área do Cliente
    path('minha-conta/', views.minha_conta, name='minha_conta'),
    path('minha-conta/dados/', views.meus_dados, name='meus_dados'),
    path('minha-conta/pedidos/', views.meus_pedidos, name='meus_pedidos'),
    path('minha-conta/rastrear/', views.rastrear_pedido, name='rastrear_pedido'),
   

    # Carrinho 
    path("carrinho/adicionar/<int:produto_id>/", views.adicionar_carrinho, name="adicionar_carrinho"),
    path("carrinho/remover/<int:produto_id>/", views.remover_carrinho, name="remover_carrinho"),
]
