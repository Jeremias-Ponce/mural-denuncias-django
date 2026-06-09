from django import forms
from django.contrib.auth.models import User
from .models import Nota

# --- Formulario de Denuncias (vinculado al modelo Nota) ---
class NotaForm(forms.ModelForm):
    class Meta:
        model = Nota
        fields = ['titulo', 'categoria', 'descripcion', 'imagen']
        # Estilos y textos de ayuda para cada campo
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ej: Farola rota'}),
            'categoria': forms.Select(attrs={'class': 'form-input'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-input', 'rows': 4, 'placeholder': 'Detalles...'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-input'})
        }

class RegistroForm(forms.Form):
    dni = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ingresa tu DNI'}))
    
    # --- CÓDIGO NUEVO ---
    # Usamos EmailField para que el navegador obligue al usuario a poner un "@"
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Tu correo electrónico'}))
    # --------------------
    
    edad = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Tu edad real'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Crea una contraseña'}))

    # Validación: Solo mayores de 18
    def clean_edad(self):
        edad = self.cleaned_data.get('edad')
        if edad < 18:
            raise forms.ValidationError("Acceso denegado: Debes ser mayor de 18 años.")
        return edad

    # Validación: Evitar DNI duplicados
    def clean_dni(self):
        dni = self.cleaned_data.get('dni')
        if User.objects.filter(username=dni).exists():
            raise forms.ValidationError("Este DNI ya se encuentra registrado.")
        return dni