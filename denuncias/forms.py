from django import forms
from django.contrib.auth.models import User
from .models import Nota

class NotaForm(forms.ModelForm):
    class Meta:
        model = Nota
        fields = ['titulo', 'categoria', 'descripcion']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ej: Farola rota'}),
            'categoria': forms.Select(attrs={'class': 'form-input'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-input', 'rows': 4, 'placeholder': 'Detalles...'}),
        }

# --- NUEVO FORMULARIO DE REGISTRO ---
class RegistroForm(forms.Form):
    dni = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ingresa tu DNI'}))
    edad = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Tu edad real'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Crea una contraseña'}))

    # Validación automática de Django para la edad
    def clean_edad(self):
        edad = self.cleaned_data.get('edad')
        if edad < 18:
            raise forms.ValidationError("Acceso denegado: Debes ser mayor de 18 años.")
        return edad

    # Validación para no repetir DNI
    def clean_dni(self):
        dni = self.cleaned_data.get('dni')
        if User.objects.filter(username=dni).exists():
            raise forms.ValidationError("Este DNI ya se encuentra registrado.")
        return dni