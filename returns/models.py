from django.db import models
from django.conf import settings
from orders.models import Order

class ReturnRequest(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    motivo = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)
