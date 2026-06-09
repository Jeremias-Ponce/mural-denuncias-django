from django.contrib import admin
from .models import Nota  # Importamos tu modelo "Nota"

# Le decimos a Django: "Registra el modelo Nota en el panel de administrador"
admin.site.register(Nota)