from django.db import models
from django.conf import settings
from products.models import Produto
import uuid

class Order(models.Model):
    STATUS_CHOICES = [
        ('P', 'Pendente'),
        ('C', 'Confirmado'),
        ('E', 'Enviado'),
        ('D', 'Entregue'),
        ('R', 'Cancelado/Devolvido'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tracking_number = models.CharField(max_length=100, blank=True)
    order_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return f"Pedido {self.order_id} - {self.user}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade = models.PositiveIntegerField()

    def subtotal(self):
        return self.preco * self.quantidade
