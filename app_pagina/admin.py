from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Categoria, Produto, Pedido, ItemPedido, Pagamento
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("usuario", "telefone", "cidade", "estado")
    search_fields = ("usuario__username", "telefone", "cidade", "estado")

# Inline de Itens do Pedido
class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0
    readonly_fields = ["produto", "quantidade", "preco_unitario"]

# Inline de Pedidos no Usuário
class PedidoInline(admin.TabularInline):
    model = Pedido
    extra = 0
    fields = ("id", "status", "valor_total", "data_pedido")
    readonly_fields = ("id", "status", "valor_total", "data_pedido")
    show_change_link = True 

# Pedido no Admin
@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ("id", "usuario", "status", "valor_total", "data_pedido")
    list_filter = ("status", "data_pedido")
    search_fields = ("usuario__username", "id")
    ordering = ("-data_pedido",)  
    inlines = [ItemPedidoInline]

# Produto no Admin
@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ("nome", "categoria", "preco_formatado", "estoque")
    list_filter = ("categoria",)
    search_fields = ("nome",)

    def preco_formatado(self, obj):
        return f"R$ {obj.preco:.2f}"
    preco_formatado.short_description = "Preço"

# Categoria no Admin
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nome",)
    search_fields = ("nome",)
    ordering = ("nome",)

# Pagamento no Admin
@admin.register(Pagamento)
class PagamentoAdmin(admin.ModelAdmin):
    list_display = ("id", "pedido", "metodo", "status", "valor_pago", "data_pagamento")
    list_filter = ("metodo", "status")
    search_fields = ("pedido__id",)
    ordering = ("-data_pagamento",)

# Customização do Usuário
class CustomUserAdmin(UserAdmin):
    inlines = [PedidoInline]


# Tira o User padrão e registra o novo
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
