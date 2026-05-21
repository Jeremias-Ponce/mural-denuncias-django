from django.db import models

class Nota(models.Model):
    # Las opciones para el menú desplegable
    CATEGORIAS = [
        ('URG', '🔴 Urgente / Peligro'),
        ('INF', '🟡 Infraestructura / Roturas'),
        ('OBS', '🔵 Observación / Comentario'),
    ]

    # Los campos que tendrá cada papelito
    titulo = models.CharField(max_length=50)
    descripcion = models.TextField(max_length=250)
    categoria = models.CharField(max_length=3, choices=CATEGORIAS, default='OBS')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} - {self.categoria}"
