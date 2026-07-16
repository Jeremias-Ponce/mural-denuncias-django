from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from .forms import NotaForm, RegistroForm
from .models import Nota


def tablero_principal(request):
    """Lista pública de denuncias, ordenadas de más reciente a más antigua."""
    notas = Nota.objects.all().order_by('-fecha_creacion')
    return render(request, 'tablero.html', {'notas': notas})


@login_required
def crear_nota(request):
    if request.method == 'POST':
        form = NotaForm(request.POST, request.FILES)
        if form.is_valid():
            nota = form.save(commit=False)
            nota.usuario = request.user
            nota.save()
            return redirect('tablero')
    else:
        form = NotaForm()

    return render(request, 'crear_nota.html', {'form': form})


@login_required
def editar_nota(request, nota_id):
    nota = get_object_or_404(Nota, id=nota_id)

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
    nota = get_object_or_404(Nota, id=nota_id)

    if nota.usuario == request.user:
        nota.delete()

    return redirect('tablero')


def registro_usuario(request):
    form = RegistroForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        dni = form.cleaned_data['dni']
        password = form.cleaned_data['password']
        email = form.cleaned_data['email']

        user = User.objects.create_user(
            username=dni,
            email=email,
            password=password,
        )
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

        error = 'DNI o contraseña incorrectos.'

    return render(request, 'login.html', {'error': error})


def logout_usuario(request):
    logout(request)
    return redirect('login')
