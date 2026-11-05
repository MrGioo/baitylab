from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from .models import EntidadVertedero, UsuarioSteam, ReporteQueja
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import RegistroUsuarioForm
from django.db.models.signals import post_save
from django.dispatch import receiver
import random

# Create your views here.
def inicio(request):
    return render(request, 'baityapp/inicio.html')

@login_required(login_url='login')
def formulario(request):
    exito = False
    if request.method == 'POST':
        form_entidad_id = request.POST.get('entidad_involucrada')
        form_tipo_estafa = request.POST.get('tipo_estafa', 'No especificado')
        form_mensaje = request.POST.get('mensaje', 'Sin mensaje')

        # Como la señal ya lo creó al registrarse, simplemente lo llamamos
        usuario_obj = UsuarioSteam.objects.get(nick_steam=request.user.username)

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
        form = RegistroUsuarioForm(request.POST) 
        if form.is_valid():
            form.save() # Al hacer save() aquí, la señal se dispara y crea el UsuarioSteam
            return redirect('login')
    else:
        form = RegistroUsuarioForm() 
        
    return render(request, 'registration/registro.html', {'form': form})



def es_admin(user):
    return user.is_superuser

@user_passes_test(es_admin, login_url='login')
def mi_panel_admin(request):
    reportes = ReporteQueja.objects.all().order_by('-fecha')
    entidades = EntidadVertedero.objects.all() # AGREGADO: Cargar entidades
    return render(request, 'baityapp/mi_panel_admin.html', {'reportes': reportes, 'entidades': entidades})

@user_passes_test(es_admin, login_url='login')
def editar_reporte_admin(request, id_reporte):
    # Actualizar (Update)
    reporte = get_object_or_404(ReporteQueja, id=id_reporte)
    entidades = EntidadVertedero.objects.all()

    if request.method == 'POST':
        entidad_id = request.POST.get('entidad_involucrada')
        reporte.entidad_involucrada = get_object_or_404(EntidadVertedero, id_entidad=entidad_id)
        reporte.tipo_estafa = request.POST.get('tipo_estafa')
        reporte.mensaje = request.POST.get('mensaje')
        reporte.save()
        return redirect('mi_panel_admin')

    return render(request, 'baityapp/admin/editar_admin.html', {'reporte': reporte, 'entidades': entidades})


@user_passes_test(es_admin, login_url='login')
def crear_entidad_admin(request):
    if request.method == 'POST':
        form_nombre = request.POST.get('nombre')
        form_categoria = request.POST.get('categoria')
        form_descripcion = request.POST.get('descripcion')
        form_imagen = request.FILES.get('imagen') # IMPORTANTE: request.FILES para la imagen

        EntidadVertedero.objects.create(
            nombre=form_nombre,
            categoria=form_categoria,
            descripcion=form_descripcion,
            imagen=form_imagen
        )
        return redirect('mi_panel_admin')

    return render(request, 'baityapp/entidad/crear_entidad.html')

@user_passes_test(es_admin, login_url='login')
def eliminar_reporte_admin(request, id_reporte):
    reporte = get_object_or_404(ReporteQueja, id=id_reporte)
    if request.method == 'POST':
        reporte.delete()
        return redirect('mi_panel_admin')
    return render(request, 'baityapp/admin/eliminar_admin.html', {'reporte': reporte})

@user_passes_test(es_admin, login_url='login')
def editar_entidad_admin(request, id_entidad):
    entidad = get_object_or_404(EntidadVertedero, id_entidad=id_entidad)
    
    if request.method == 'POST':
        entidad.nombre = request.POST.get('nombre')
        entidad.categoria = request.POST.get('categoria')
        entidad.descripcion = request.POST.get('descripcion')
        
        # Solo actualizamos la imagen si el usuario subió una nueva
        if request.FILES.get('imagen'):
            entidad.imagen = request.FILES.get('imagen')
            
        entidad.save()
        return redirect('mi_panel_admin')

    return render(request, 'baityapp/entidad/editar_entidad.html', {'entidad': entidad})

@user_passes_test(es_admin, login_url='login')
def eliminar_entidad_admin(request, id_entidad):
    entidad = get_object_or_404(EntidadVertedero, id_entidad=id_entidad)
    if request.method == 'POST':
        entidad.delete()
        return redirect('mi_panel_admin')
    return render(request, 'baityapp/entidad/eliminar_entidad.html', {'entidad': entidad})

@user_passes_test(es_admin, login_url='login')
def mi_panel_admin(request):
    # 1. Capturar los filtros de la URL (GET)
    filtro_estudio = request.GET.get('estudio')
    filtro_tipo = request.GET.get('tipo')

    reportes = ReporteQueja.objects.all().order_by('-fecha')

    # 2. Aplicar los filtros si el usuario seleccionó alguno
    if filtro_estudio:
        reportes = reportes.filter(entidad_involucrada__id_entidad=filtro_estudio)
    if filtro_tipo:
        reportes = reportes.filter(tipo_estafa=filtro_tipo)

    entidades = EntidadVertedero.objects.all()
    usuarios = UsuarioSteam.objects.all() # CARGAR USUARIOS

    return render(request, 'baityapp/mi_panel_admin.html', {
        'reportes': reportes, 
        'entidades': entidades, 
        'usuarios': usuarios,
        'filtro_estudio': filtro_estudio,
        'filtro_tipo': filtro_tipo
    })

@user_passes_test(es_admin, login_url='login')
def editar_usuario_admin(request, id_usuario):
    # La primary key es id_usuario (tipo string)
    usuario_steam = get_object_or_404(UsuarioSteam, id_usuario=id_usuario)
    
    if request.method == 'POST':
        usuario_steam.nick_steam = request.POST.get('nick_steam')
        usuario_steam.correo = request.POST.get('correo')
        usuario_steam.save()
        return redirect('mi_panel_admin')

    return render(request, 'baityapp/usuario/editar_usuario.html', {'usuario_steam': usuario_steam})

@user_passes_test(es_admin, login_url='login')
def eliminar_usuario_admin(request, id_usuario):
    usuario_steam = get_object_or_404(UsuarioSteam, id_usuario=id_usuario)
    
    if request.method == 'POST':
        # Guardamos el nick antes de borrar para buscarlo en la tabla nativa
        nick_a_borrar = usuario_steam.nick_steam
        
        # 1. Borramos el perfil de UsuarioSteam (y sus reportes en cascada)
        usuario_steam.delete()
        
        # 2. Buscamos y aniquilamos la cuenta nativa de Django para que no pueda loguearse más
        try:
            cuenta_nativa = User.objects.get(username=nick_a_borrar)
            cuenta_nativa.delete()
        except User.DoesNotExist:
            pass # Si por alguna razón no existe, no hacemos que la página colapse
            
        return redirect('mi_panel_admin')
        
    return render(request, 'baityapp/usuario/eliminar_usuario.html', {'usuario_steam': usuario_steam})


@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    if created: # Solo si es un usuario NUEVO
        UsuarioSteam.objects.create(
            id_usuario=str(instance.id).zfill(8),
            nick_steam=instance.username,
            correo=instance.email)