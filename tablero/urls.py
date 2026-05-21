from django.contrib import admin
from django.urls import path
from denuncias.views import tablero_principal, crear_nota

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', tablero_principal, name='tablero'),             # Página de inicio (Mural)
    path('nueva-denuncia/', crear_nota, name='crear_nota'),  # Página del formulario
]