from django.db import models
from django.contrib.auth.models import User 

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
    imagen = models.ImageField(upload_to='denuncias_fotos/', null=True, blank=True)

    def __str__(self):
        return f"{self.titulo} - {self.categoria}"            