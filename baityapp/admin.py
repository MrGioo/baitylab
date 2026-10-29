from django.contrib import admin
from .models import UsuarioSteam, EntidadVertedero, ReporteQueja

@admin.register(ReporteQueja)
class ReporteQuejaAdmin(admin.ModelAdmin):
    # Añadimos 'mensaje' a las columnas visibles
    list_display = ('id', 'usuario', 'entidad_involucrada', 'tipo_estafa', 'mensaje', 'fecha')
    
    list_filter = ('entidad_involucrada', 'tipo_estafa', 'fecha')
    search_fields = ('usuario__nick_steam', 'mensaje')
    ordering = ('-fecha',)
    readonly_fields = ('fecha',)
    list_per_page = 20

@admin.register(EntidadVertedero)
class EntidadVertederoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria')
    search_fields = ('nombre', 'categoria')
    list_filter = ('categoria',)

@admin.register(UsuarioSteam)
class UsuarioSteamAdmin(admin.ModelAdmin):
    list_display = ('nick_steam', 'correo', 'id_usuario')
    search_fields = ('nick_steam', 'correo')