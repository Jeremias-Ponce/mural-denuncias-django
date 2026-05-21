from django import forms
from .models import Nota

class NotaForm(forms.ModelForm):
    class Meta:
        model = Nota
        fields = ['titulo', 'categoria', 'descripcion']
        
        # Aquí le damos un poco de estilo y textos de ayuda a las cajas donde el usuario escribe
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-input', 
                'placeholder': 'Ej: Farola rota en la plaza'
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-input'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-input', 
                'rows': 4, 
                'placeholder': 'Describe el detalle aquí...'
            }),
        }