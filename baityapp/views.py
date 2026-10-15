from django.shortcuts import render
from django.http import HttpResponse
from .models import EntidadVertedero

# Create your views here.
def inicio(request):
    return render(request, 'baityapp/inicio.html')

def formulario(request):
    return render(request, 'baityapp/formulario.html')

def galeria(request):
    # Traemos todas las entidades creadas directamente desde la base de datos
    elementos = EntidadVertedero.objects.all()
    
    # Pasamos los elementos correctamente a tu template de la app
    return render(request, 'baityapp/galeria.html', {'elementos': elementos})