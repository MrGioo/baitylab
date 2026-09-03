from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def inicio(request):
    return render(request, 'baityapp/inicio.html')

def formulario(request):
    return render(request, 'baityapp/formulario.html')

def galeria(request):
    elementos = [
        {
            'nombre': 'Activision',
            'raza': 'Publisher',
            'descripcion': 'Famosos por los pases de batalla.',
            'imagen': 'images/Activision-Symbol.avif'
        },
        {
            'nombre': 'Bethesda',
            'raza': 'Estudio',
            'descripcion': 'El hogar de los bugs del Día 1.',
            'imagen': 'images/bethesda-game-studios-1.avif'
        },
        {
            'nombre': 'Electronic Arts',
            'raza': 'Publisher',
            'descripcion': 'Micropagos por todas partes.',
            'imagen': 'images/Electronic-Arts-games.avif'
        },
        {
            'nombre': 'Omori',
            'raza': 'Indie',
            'descripcion': 'Gráficos y depresión.',
            'imagen': 'images/juegoomori.avif'
        },
        {
            'nombre': 'Vaca',
            'raza': 'Asset',
            'descripcion': 'Motor gráfico de pruebas.',
            'imagen': 'images/vaca.avif'
        },
    ]
    
    # Pasamos los elementos correctamente a tu template de la app
    return render(request, 'baityapp/galeria.html', {'elementos': elementos})
