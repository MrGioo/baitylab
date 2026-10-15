from django.http import HttpResponse
from django.shortcuts import render
from .models import EntidadVertedero, UsuarioSteam, ReporteQueja
import random

# Create your views here.
def inicio(request):
    return render(request, 'baityapp/inicio.html')


def formulario(request):
    if request.method == 'POST':
        # Ya no capturamos el id_usuario, solo el nick y el correo
        form_nick = request.POST.get('nick_steam', 'Anonimo')
        form_correo = request.POST.get('correo', 'sin@correo.com')
        
        form_entidad_id = request.POST.get('entidad_involucrada')
        form_tipo_estafa = request.POST.get('tipo_estafa', 'No especificado')
        form_mensaje = request.POST.get('mensaje', 'Sin mensaje')

        # Buscamos al usuario por su CORREO. 
        # Si no existe, lo crea y le inventa un ID aleatorio de 8 números.
        id_aleatorio = str(random.randint(10000000, 99999999))
        
        usuario_obj, creado = UsuarioSteam.objects.get_or_create(
            correo=form_correo,
            defaults={
                'id_usuario': id_aleatorio, 
                'nick_steam': form_nick
            }
        )

        # Buscamos la entidad y creamos el reporte
        try:
            entidad_obj = EntidadVertedero.objects.get(id_entidad=form_entidad_id)
            
            ReporteQueja.objects.create(
                usuario=usuario_obj,
                entidad_involucrada=entidad_obj,
                tipo_estafa=form_tipo_estafa,
                mensaje=form_mensaje
            )
            return render(request, 'baityapp/formulario.html', {'exito': True})
            
        except EntidadVertedero.DoesNotExist:
            # Por si algo falla con la entidad
            pass

    entidades = EntidadVertedero.objects.all()
    return render(request, 'baityapp/formulario.html', {'entidades': entidades})

def galeria(request):
    # Traemos todas las entidades creadas directamente desde la base de datos
    elementos = EntidadVertedero.objects.all()
    
    # Pasamos los elementos correctamente a tu template de la app
    return render(request, 'baityapp/galeria.html', {'elementos': elementos})