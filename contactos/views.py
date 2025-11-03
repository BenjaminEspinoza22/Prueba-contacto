from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Contacto
from .forms import ContactoForm

def lista_contactos(request):
    contactos = Contacto.objects.all()
    
    # Búsqueda usando estructura de decisión
    query = request.GET.get('q')
    if query:
        contactos = contactos.filter(
            Q(nombre__icontains=query) | 
            Q(correo__icontains=query) |
            Q(telefono__icontains=query)
        )
    
    context = {
        'contactos': contactos,
        'query': query,
        'total_contactos': contactos.count()
    }
    
    return render(request, 'contactos/lista_contactos.html', context)

def agregar_contacto(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_contactos')
    else:
        form = ContactoForm()
    
    return render(request, 'contactos/agregar_contacto.html', {'form': form})

def editar_contacto(request, contacto_id):
    contacto = get_object_or_404(Contacto, id=contacto_id)
    
    if request.method == 'POST':
        form = ContactoForm(request.POST, instance=contacto)
        if form.is_valid():
            form.save()
            return redirect('lista_contactos')
    else:
        form = ContactoForm(instance=contacto)
    
    # CORRECCIÓN: Pasar tanto 'form' como 'contacto'
    return render(request, 'contactos/editar_contacto.html', {
        'form': form, 
        'contacto': contacto
    })

def eliminar_contacto(request, contacto_id):
    contacto = get_object_or_404(Contacto, id=contacto_id)
    
    if request.method == 'POST':
        contacto.delete()
        return redirect('lista_contactos')
    
    return render(request, 'contactos/eliminar_contacto.html', {'contacto': contacto})

def detalle_contacto(request, contacto_id):
    contacto = get_object_or_404(Contacto, id=contacto_id)
    return render(request, 'contactos/detalle_contacto.html', {'contacto': contacto})