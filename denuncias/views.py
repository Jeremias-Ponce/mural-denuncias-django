from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from .forms import NotaForm, RegistroForm
from .models import Nota

# --- VISTAS PÚBLICAS ---

def tablero_principal(request):
    """Muestra todas las denuncias en orden cronológico inverso (lo último primero)."""
    notas = Nota.objects.all().order_by('-fecha_creacion')
    return render(request, 'tablero.html', {'notas': notas})

# --- VISTAS PROTEGIDAS (Requieren inicio de sesión) ---

@login_required
def crear_nota(request):
    """Maneja la creación de nuevas denuncias asociándolas al usuario logueado."""
    if request.method == 'POST':
        # Procesamos los datos y la imagen enviada
        form = NotaForm(request.POST, request.FILES)
        if form.is_valid():
            nota = form.save(commit=False) # Creamos el objeto sin guardar aún en la BD
            nota.usuario = request.user    # Asignamos el autor automáticamente
            nota.save()                    # Guardamos finalmente
            return redirect('tablero')
    else:
        form = NotaForm()

    return render(request, 'crear_nota.html', {'form': form})


@login_required
def editar_nota(request, nota_id):
    """Permite editar una nota solo si el usuario actual es su autor original."""
    nota = get_object_or_404(Nota, id=nota_id)

    # Verificación de seguridad: si no eres el autor, no puedes editar
    if nota.usuario != request.user:
        return redirect('tablero')

    if request.method == 'POST':
        form = NotaForm(request.POST, request.FILES, instance=nota)
        if form.is_valid():
            form.save()
            return redirect('tablero')
    else:
        form = NotaForm(instance=nota)

    return render(request, 'editar_nota.html', {'form': form})


@login_required
def eliminar_nota(request, nota_id):
    """Borra una nota tras verificar que el usuario tenga los permisos necesarios."""
    nota = get_object_or_404(Nota, id=nota_id)

    # Validamos que solo el dueño pueda eliminar su propio reporte
    if nota.usuario == request.user:
        nota.delete()

    return redirect('tablero')

# --- VISTAS DE AUTENTICACIÓN ---

def registro_usuario(request):
    """Crea una cuenta nueva utilizando el DNI como nombre de usuario."""
    form = RegistroForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        dni = form.cleaned_data['dni']
        password = form.cleaned_data['password']
        email = form.cleaned_data['email']

        # Creamos el usuario en la base de datos y lo logueamos al instante
        user = User.objects.create_user(
            username=dni,
            email=email,
            password=password,
        )
        login(request, user)
        return redirect('tablero')

    return render(request, 'registro.html', {'form': form})


def login_usuario(request):
    """Valida las credenciales ingresadas contra la base de datos."""
    error = None

    if request.method == 'POST':
        dni = request.POST.get('dni')
        password = request.POST.get('password')
        # authenticate verifica contra la base de datos de usuarios de Django
        user = authenticate(request, username=dni, password=password)

        if user is not None:
            login(request, user)
            return redirect('tablero')

        # Si no existe, preparamos un mensaje de error
        error = 'DNI o contraseña incorrectos.'

    return render(request, 'login.html', {'error': error})


def logout_usuario(request):
    """Cierra la sesión actual y redirige al usuario a la pantalla de login."""
    logout(request)
    return redirect('login')