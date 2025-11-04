from django.db import models
from django.contrib.auth.models import User

# Categoria
class Categoria(models.Model):
    nome = models.CharField("Nome da Categoria", max_length=100, unique=True)
    descricao = models.TextField("Descrição", blank=True, null=True)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ["nome"]  # ordena alfabeticamente

    def __str__(self):
        return self.nome

# Produto
class Produto(models.Model):
    nome = models.CharField("Nome do Produto", max_length=150)
    descricao = models.TextField("Descrição")
    preco = models.DecimalField("Preço", max_digits=8, decimal_places=2)
    estoque = models.PositiveIntegerField("Estoque", default=0)
    imagem = models.ImageField("Imagem", upload_to="produtos/")
    categoria = models.ForeignKey(
        Categoria, on_delete=models.CASCADE, related_name="produtos", verbose_name="Categoria"
    )

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        ordering = ["nome"]

    def __str__(self):
        return f"{self.nome} (R$ {self.preco:.2f})"

# Pedido
class Pedido(models.Model):
    STATUS_CHOICES = [
        ("aguardando", "Aguardando Pagamento"),
        ("pago", "Pago"),
        ("enviado", "Enviado"),
        ("entregue", "Entregue"),
        ("cancelado", "Cancelado"),
    ]

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="pedidos",
        null=True,
        blank=True,
        verbose_name="Usuário"
    )   

    data_pedido = models.DateTimeField("Data do Pedido", auto_now_add=True)
    status = models.CharField("Status", max_length=20, choices=STATUS_CHOICES, default="aguardando")
    valor_total = models.DecimalField("Valor Total", max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ["-data_pedido"]  
    def __str__(self):
        usuario_nome = self.usuario.username if self.usuario else "Usuário Anônimo"
        return f"Pedido {self.id} - {usuario_nome} - {self.get_status_display()}"

# Item do Pedido
class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="itens")
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField("Quantidade", default=1)
    preco_unitario = models.DecimalField(max_digits=8, decimal_places=2, default=0)


    class Meta:
        verbose_name = "Item do Pedido"
        verbose_name_plural = "Itens do Pedido"

    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome} (Pedido {self.pedido.id})"
    
# Pagamento
class Pagamento(models.Model):
    METODOS = [
        ("cartao", "Cartão de Crédito"),
        ("pix", "PIX"),
        ("boleto", "Boleto"),
    ]

    STATUS_CHOICES = [
        ("pendente", "Pendente"),
        ("pago", "Pago"),
        ("recusado", "Recusado"),
    ]

    pedido = models.OneToOneField(
        Pedido, on_delete=models.CASCADE, related_name="pagamento", verbose_name="Pedido"
    )
    metodo = models.CharField("Método de Pagamento", max_length=20, choices=METODOS)
    status = models.CharField("Status", max_length=20, choices=STATUS_CHOICES, default="pendente")
    valor_pago = models.DecimalField("Valor Pago", max_digits=10, decimal_places=2, default=0)
    data_pagamento = models.DateTimeField("Data do Pagamento", blank=True, null=True)

    class Meta:
        verbose_name = "Pagamento"
        verbose_name_plural = "Pagamentos"
        ordering = ["-data_pagamento"]

    def __str__(self):
        return f"Pagamento {self.id} - {self.get_metodo_display()} - {self.get_status_display()}"
    
# Perfil do Usuário 
class UserProfile(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name="perfil")
    telefone = models.CharField(max_length=20, blank=True, null=True)
    endereco = models.CharField(max_length=255, blank=True, null=True)
    cidade = models.CharField(max_length=100, blank=True, null=True)
    estado = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"Perfil de {self.usuario.username}"
