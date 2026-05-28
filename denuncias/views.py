from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Nota
from .forms import NotaForm, RegistroForm

#Nota.objects.all(): Le dice a la base de datos "Tráeme TODOS los papelitos de denuncias".

#.order_by('-fecha_creacion'): Ese signo menos (-) es clave. Significa que los ordene de más nuevo a más viejo. Así, la última denuncia que se haga aparecerá primera arriba de todo.

#return render(...): Agarra todas esas notas que sacó de la base de datos, las envuelve en tu diseño tablero.html y se las muestra al usuario.

@login_required
def tablero_principal(request):
    notas = Nota.objects.all().order_by('-fecha_creacion')
    return render(request, 'tablero.html', {'notas': notas})

@login_required
def crear_nota(request):
    if request.method == 'POST':
        form = NotaForm(request.POST)
        if form.is_valid():
            nota = form.save(commit=False)
            nota.usuario = request.user  # Asigna la nota al usuario logueado
            nota.save()
            return redirect('tablero')
    else:
        form = NotaForm()
    return render(request, 'crear_nota.html', {'form': form})

# --- ELIMINAR NOTA PROPIA ---
@login_required
def eliminar_nota(request, nota_id):
    nota = get_object_or_404(Nota, id=nota_id)
    # Seguridad: Solo el que la creó puede borrarla
    if nota.usuario == request.user:
        nota.delete()
    return redirect('tablero')

# --- VISTAS DE CONTROL DE ACCESO ---
def registro_usuario(request):
    form = RegistroForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        dni = form.cleaned_data['dni']
        password = form.cleaned_data['password']
        # Guardamos el DNI dentro del campo username interno de Django
        user = User.objects.create_user(username=dni, password=password)
        login(request, user)
        return redirect('tablero')
    return render(request, 'registro.html', {'form': form})

def login_usuario(request):
    error = None
    if request.method == 'POST':
        dni = request.POST.get('dni')
        password = request.POST.get('password')
        user = authenticate(request, username=dni, password=password)
        if user is not None:
            login(request, user)
            return redirect('tablero')
        error = "DNI o contraseña incorrectos."
    return render(request, 'login.html', {'error': error})

def logout_usuario(request):
    logout(request)
    return redirect('login')