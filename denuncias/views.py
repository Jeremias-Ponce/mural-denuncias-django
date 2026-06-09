from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Nota
from .forms import NotaForm, RegistroForm

# =========================================================
# 1. TABLERO PRINCIPAL (La pantalla de inicio)
# =========================================================
# @login_required es el "patovica". Si no iniciaste sesión, te patea al login.
@login_required
def tablero_principal(request):
    # Le dice a la base de datos "Tráeme TODOS los papelitos de denuncias".
    # El signo menos (-) en '-fecha_creacion' es para ordenarlos del más nuevo al más viejo.
    notas = Nota.objects.all().order_by('-fecha_creacion')
    
    # Agarra esas notas, las envuelve en el diseño HTML y se las muestra al usuario.
    return render(request, 'tablero.html', {'notas': notas})


# =========================================================
# 2. CREAR UNA NUEVA NOTA
# =========================================================
@login_required
def crear_nota(request):
    # Si el método es POST (significa que el usuario presionó el botón "Enviar" en el HTML)
    if request.method == 'POST':
        # Agarramos los datos que vienen en ese "sobre cerrado"
        form = NotaForm(request.POST, request.FILES)
        
        # Verificamos que no haya trampas y los datos sean válidos
        if form.is_valid():
            # commit=False significa: "Prepara la nota, pero haz una pausa, ¡aún no la guardes!"
            nota = form.save(commit=False)
            
            # Durante la pausa, le estampamos la firma del usuario logueado en secreto por seguridad
            nota.usuario = request.user  
            
            # Ahora sí, la guardamos definitivamente en la base de datos
            nota.save()
            
            # Lo redirigimos al tablero principal para que vea su nueva nota
            return redirect('tablero')
    else:
        # Si el método es GET (el usuario recién entró a la página), le damos el formulario vacío
        form = NotaForm()
        
    return render(request, 'crear_nota.html', {'form': form})


# =========================================================
# 3. ELIMINAR NOTA PROPIA
# =========================================================
@login_required
def eliminar_nota(request, nota_id):
    # get_object_or_404: Busca la nota por su número de ID. Si no existe, tira la página de Error 404.
    nota = get_object_or_404(Nota, id=nota_id)
    
    # Control de Seguridad vital: Comparamos al creador de la nota con el usuario actual.
    # Solo si coinciden (es decir, el usuario es el dueño original), se procede a borrarla.
    if nota.usuario == request.user:
        nota.delete()
        
    # Devuelve al usuario a la pantalla principal
    return redirect('tablero')


# =========================================================
# 4. VISTAS DE CONTROL DE ACCESO (SISTEMA DE USUARIOS)
# =========================================================

# --- REGISTRO DE NUEVOS CIUDADANOS ---
def registro_usuario(request):
    # Preparamos el formulario personalizado
    form = RegistroForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        # Extraemos los datos limpios
        dni = form.cleaned_data['dni']
        password = form.cleaned_data['password']
        
        # --- CÓDIGO NUEVO ---
        # Atrapamos el correo que el usuario escribió
        email = form.cleaned_data['email'] 
        
        # Le pasamos el email al creador de usuarios (fíjate que agregamos email=email adentro de los paréntesis)
        user = User.objects.create_user(username=dni, email=email, password=password)
        # --------------------
        
        login(request, user)
        return redirect('tablero')
        
    return render(request, 'registro.html', {'form': form})


# --- INICIO DE SESIÓN (LOGIN) ---
def login_usuario(request):
    error = None
    if request.method == 'POST':
        # Agarramos lo que el usuario escribió en las cajitas de texto
        dni = request.POST.get('dni')
        password = request.POST.get('password')
        
        # authenticate: Va a la base de datos a comprobar si ese DNI y contraseña coinciden
        user = authenticate(request, username=dni, password=password)
        
        # Si el usuario existe y los datos están bien (no es None)
        if user is not None:
            # Le da la tarjeta de acceso (sesión) y lo deja pasar al tablero
            login(request, user)
            return redirect('tablero')
            
        # Si se equivocó, preparamos este mensaje de error para mostrarlo en el HTML
        error = "DNI o contraseña incorrectos."
        
    return render(request, 'login.html', {'error': error})


# --- CERRAR SESIÓN (LOGOUT) ---
def logout_usuario(request):
    # Destruye la sesión actual por seguridad
    logout(request)
    # Lo devuelve a la pantalla de login
    return redirect('login')