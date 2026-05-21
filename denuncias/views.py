from django.shortcuts import render, redirect
from .models import Nota
from .forms import NotaForm

def tablero_principal(request):
    # Trae todas las notas ordenadas por fecha (la más reciente primero)
    notas = Nota.objects.all().order_by('-fecha_creacion')
    return render(request, 'tablero.html', {'notas': notas})

def crear_nota(request):
    # Si el usuario envió el formulario (presionó el botón de enviar)
    if request.method == 'POST':
        form = NotaForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda los datos de forma segura en la base de datos
            return redirect('tablero')  # Redirige automáticamente al mural principal
    else:
        # Si el usuario solo entró a ver la página, le entrega el formulario vacío
        form = NotaForm()
    
    return render(request, 'crear_nota.html', {'form': form})