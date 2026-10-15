from django.contrib import admin

# Register your models here.

from .models import UsuarioSteam, EntidadVertedero, ReporteQueja

admin.site.register(UsuarioSteam)
admin.site.register(EntidadVertedero)
admin.site.register(ReporteQueja)