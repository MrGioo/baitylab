from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required  # Falta esta importación clave
from .models import EntidadVertedero, UsuarioSteam, ReporteQueja
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import RegistroUsuarioForm 

import random

# Create your views here.
def inicio(request):
    return render(request, 'baityapp/inicio.html')

@login_required(login_url='login')
def formulario(request):
    exito = False
    if request.method == 'POST':
        # 1. Tomamos los datos de forma segura desde la sesión de Django
        correo_usuario = request.user.email
        nick_usuario = request.user.username
        
        form_entidad_id = request.POST.get('entidad_involucrada')
        form_tipo_estafa = request.POST.get('tipo_estafa', 'No especificado')
        form_mensaje = request.POST.get('mensaje', 'Sin mensaje')

        # 2. Buscamos el usuario en lugar de crearlo a ciegas.
        try:
            usuario_obj = UsuarioSteam.objects.get(correo=correo_usuario)
        except UsuarioSteam.DoesNotExist:
            usuario_obj = UsuarioSteam.objects.create(
                id_usuario=str(request.user.id).zfill(8),
                nick_steam=nick_usuario,
                correo=correo_usuario
            )

        # 3. Guardamos el reporte
        try:
            entidad_obj = EntidadVertedero.objects.get(id_entidad=form_entidad_id)
            ReporteQueja.objects.create(
                usuario=usuario_obj,
                entidad_involucrada=entidad_obj,
                tipo_estafa=form_tipo_estafa,
                mensaje=form_mensaje
            )
            exito = True
        except EntidadVertedero.DoesNotExist:
            pass

    entidades = EntidadVertedero.objects.all()
    return render(request, 'baityapp/formulario.html', {'entidades': entidades, 'exito': exito})

def galeria(request):
    # Traemos todas las entidades creadas directamente desde la base de datos
    elementos = EntidadVertedero.objects.all()
    
    # Pasamos los elementos correctamente a tu template de la app
    return render(request, 'baityapp/galeria.html', {'elementos': elementos})

def registro(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST) # Usa el nuevo formulario aquí
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistroUsuarioForm() # Y aquí también
        
    return render(request, 'registration/registro.html', {'form': form})