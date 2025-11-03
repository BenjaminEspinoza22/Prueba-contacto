from django.urls import path
from . import views

# app_name = 'contactos'

urlpatterns = [
    path('', views.lista_contactos, name='lista_contactos'),
    path('agregar/', views.agregar_contacto, name='agregar_contacto'),
    path('editar/<int:contacto_id>/', views.editar_contacto, name='editar_contacto'),
    path('eliminar/<int:contacto_id>/', views.eliminar_contacto, name='eliminar_contacto'),
    path('detalle/<int:contacto_id>/', views.detalle_contacto, name='detalle_contacto'),
]