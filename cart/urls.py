from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='detail'),
    path('add/<int:produto_id>/', views.add_to_cart, name='add'),
    path('remove/<int:produto_id>/', views.remove_from_cart, name='remove'),
    path('checkout/', views.checkout, name='checkout'),
]