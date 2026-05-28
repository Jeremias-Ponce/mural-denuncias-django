from django import forms
from django.contrib.auth.models import User
from .models import Nota

# =========================================================
# 1. FORMULARIO DE NOTAS / DENUNCIAS (Basado en el Modelo)
# =========================================================
# Usamos forms.ModelForm porque queremos que Django arme el formulario
# automáticamente leyendo las reglas que ya pusimos en models.py.
class NotaForm(forms.ModelForm):
    
    # La clase Meta es la "Sala de Configuración" del formulario.
    class Meta:
        model = Nota  # Le indicamos cuál es la caja fuerte (el modelo) a usar.
        
        # Elegimos estrictamente qué campos mostrarle al vecino.
        # (Ocultamos el usuario y la fecha por seguridad, eso lo maneja el sistema).
        fields = ['titulo', 'categoria', 'descripcion']
        
        # Los 'widgets' son el maquillaje visual. 
        # Aquí le inyectamos desde Python las clases de tu CSS ('form-input') 
        # y los textos de ayuda (placeholders) para no tener que ensuciar el HTML.
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ej: Farola rota'}),
            'categoria': forms.Select(attrs={'class': 'form-input'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-input', 'rows': 4, 'placeholder': 'Detalles...'}),
        }

# =========================================================
# 2. NUEVO FORMULARIO DE REGISTRO (Formulario Libre)
# =========================================================
# Usamos forms.Form (y no ModelForm) porque este formulario lo armamos
# nosotros desde cero a medida, no copia directamente una tabla.
class RegistroForm(forms.Form):
    
    # Dibujamos las tres cajitas que verá el usuario en la pantalla:
    dni = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ingresa tu DNI'}))
    
    # NumberInput fuerza a que el usuario solo pueda escribir números.
    edad = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Tu edad real'}))
    
    # PasswordInput es vital: convierte el texto en asteriscos (***) por privacidad.
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Crea una contraseña'}))

    # =========================================================
    # LOS GUARDIANES DE SEGURIDAD (Validaciones)
    # Cualquier función que empiece con "clean_" revisa el dato ANTES de guardarlo.
    # =========================================================

    # Guardián 1: Verificador de Edad
    def clean_edad(self):
        # Agarramos la edad que escribió la persona
        edad = self.cleaned_data.get('edad')
        
        # Regla de negocio: Si tiene menos de 18, bloqueamos el proceso.
        if edad < 18:
            # ValidationError es la "bomba de humo" que detiene todo y muestra el texto en rojo.
            raise forms.ValidationError("Acceso denegado: Debes ser mayor de 18 años.")
            
        # Si todo está bien, dejamos pasar el dato.
        return edad

    # Guardián 2: Verificador de Duplicados en la Base de Datos
    def clean_dni(self):
        # Agarramos el DNI que escribió la persona
        dni = self.cleaned_data.get('dni')
        
        # Le preguntamos a la base de usuarios de Django si ya existe alguien con este DNI (username)
        if User.objects.filter(username=dni).exists():
            # Si la respuesta es Sí, detenemos el registro para evitar cuentas duplicadas.
            raise forms.ValidationError("Este DNI ya se encuentra registrado.")
            
        # Si no existe, el DNI está libre y lo dejamos pasar.
        return dni