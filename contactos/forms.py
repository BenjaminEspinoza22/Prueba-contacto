from django import forms
from .models import Contacto

class ContactoForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = ['nombre', 'telefono', 'correo', 'direccion']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'placeholder': 'Ingrese nombre completo'
            }),
            'telefono': forms.TextInput(attrs={
                'placeholder': 'Ej: +56 9 1234 5678'
            }),
            'correo': forms.EmailInput(attrs={
                'placeholder': 'Ej: contacto@ejemplo.com'
            }),
            'direccion': forms.Textarea(attrs={
                'placeholder': 'Ingrese dirección completa',
                'rows': 3
            })
        }
    
    def clean_correo(self):
        correo = self.cleaned_data['correo']
        contacto = Contacto()
        
        if not contacto.validar_correo(correo):
            raise forms.ValidationError('Formato de correo electrónico inválido')
        
        return correo
    
    def clean_telefono(self):
        telefono = self.cleaned_data['telefono']
        contacto = Contacto()
        
        if not contacto.validar_telefono(telefono):
            raise forms.ValidationError('Formato de teléfono inválido. Use: +56 9 1234 5678')
        
        return telefono
    
    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        
        if len(nombre.strip()) < 2:
            raise forms.ValidationError('El nombre debe tener al menos 2 caracteres')
        
        return nombre.strip()