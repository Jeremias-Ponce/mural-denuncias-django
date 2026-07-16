from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

from denuncias import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.tablero_principal, name='tablero'),
    path('nueva-denuncia/', views.crear_nota, name='crear_nota'),
    path('editar/<int:nota_id>/', views.editar_nota, name='editar_nota'),
    path('eliminar/<int:nota_id>/', views.eliminar_nota, name='eliminar_nota'),
    path('registro/', views.registro_usuario, name='registro'),
    path('login/', views.login_usuario, name='login'),
    path('logout/', views.logout_usuario, name='logout'),
    path(
        'reset_password/',
        auth_views.PasswordResetView.as_view(
            template_name='recuperacion/password_reset_form.html',
        ),
        name='password_reset',
    ),
    path(
        'reset_password_sent/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='recuperacion/password_reset_done.html',
        ),
        name='password_reset_done',
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='recuperacion/password_reset_confirm.html',
        ),
        name='password_reset_confirm',
    ),
    path(
        'reset_password_complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='recuperacion/password_reset_complete.html',
        ),
        name='password_reset_complete',
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
