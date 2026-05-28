from django.contrib import admin
from django.urls import path
from denuncias import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.tablero_principal, name='tablero'),
    path('nueva-denuncia/', views.crear_nota, name='crear_nota'),
    path('eliminar/<int:nota_id>/', views.eliminar_nota, name='eliminar_nota'),
    path('registro/', views.registro_usuario, name='registro'),
    path('login/', views.login_usuario, name='login'),
    path('logout/', views.logout_usuario, name='logout'),
]