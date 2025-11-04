from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Esta linha aponta para a URL do painel de administração
    path('admin/', admin.site.urls),
    
    # Esta linha inclui todas as URLs da sua app (app_pagina)
    path('', include('app_pagina.urls')),
    path('produtos/', include('products.urls')),
    path('cart/', include('cart.urls')),
    path('orders/', include('orders.urls')),
    path('perfil/', include('profiles.urls')),
    path('contacts/', include('contacts.urls')),
]

# Configuração para servir arquivos de mídia (imagens) durante o desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)