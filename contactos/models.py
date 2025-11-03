from django.db import models
from django.core.exceptions import ValidationError
import re

class Contacto(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    correo = models.EmailField(max_length=100)
    direccion = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    def clean(self):
        # Validar formato de correo usando estructura de decisión
        if not self.validar_correo(self.correo):
            raise ValidationError({'correo': 'Formato de correo electrónico inválido'})
        
        # Validar formato de teléfono
        if not self.validar_telefono(self.telefono):
            raise ValidationError({'telefono': 'Formato de teléfono inválido'})
    
    def validar_correo(self, correo):
        """Valida el formato del correo electrónico"""
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(patron, correo) is not None
    
    def validar_telefono(self, telefono):
        """Valida el formato del teléfono"""
        # Permite formatos: +56 9 1234 5678, 56912345678, 12345678
        patron = r'^(\+?56\s?9?\s?)?[0-9]{8,9}$'
        telefono_limpio = telefono.replace(' ', '')
        return re.match(patron, telefono_limpio) is not None
    
    def __str__(self):
        return f"{self.nombre} - {self.correo}"

    class Meta:
        verbose_name = 'Contacto'
        verbose_name_plural = 'Contactos'
        ordering = ['nombre']