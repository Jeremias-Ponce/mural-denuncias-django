from django.db import models #Le dice a Python: "Tráeme la caja de herramientas de Django que sirve para construir bases de datos".
from django.contrib.auth.models import User  # Django es muy inteligente y ya viene con un sistema de usuarios completo (con contraseñas, encriptación, etc.) guardado en una tabla llamada User. Aquí simplemente estamos trayendo esa tabla prefabricada para poder conectarla con nuestros papelitos.

class Nota(models.Model): #Aquí le estamos diciendo a Django: "Crea una tabla en la base de datos y llámala Nota". Cada vez que alguien llene el formulario en tu web, se creará una nueva fila dentro de esta tabla.
    CATEGORIAS = [
        ('URG', '🔴 Urgente / Peligro'),
        ('INF', '🟡 Infraestructura / Roturas'),
        ('OBS', '🔵 Observación / Comentario'),
    ]

    # Vincula la nota con un usuario. Si el usuario se borra, se borran sus notas.
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    titulo = models.CharField(max_length=50) 
    descripcion = models.TextField(max_length=250)
    categoria = models.CharField(max_length=3, choices=CATEGORIAS, default='OBS') 
    fecha_creacion = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"{self.titulo} - {self.categoria}"            