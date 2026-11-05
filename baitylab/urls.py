from django.contrib import admin
from django.urls import path, include
from baityapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inicio, name='inicio'),
    path('galeria/', views.galeria, name='galeria'),      
    path('formulario/', views.formulario, name='formulario'),
    path('registro/', views.registro, name='registro'), 
    path('accounts/',include('django.contrib.auth.urls')),
    path('mi-panel/', views.mi_panel_admin, name='mi_panel_admin'),
    path('mi-panel/editar/<int:id_reporte>/', views.editar_reporte_admin, name='editar_reporte_admin'),
    path('mi-panel/eliminar/<int:id_reporte>/', views.eliminar_reporte_admin, name='eliminar_reporte_admin'),
    path('mi-panel/entidad/nueva/', views.crear_entidad_admin, name='crear_entidad_admin'),
    path('mi-panel/entidad/editar/<int:id_entidad>/', views.editar_entidad_admin, name='editar_entidad_admin'),
    path('mi-panel/entidad/eliminar/<int:id_entidad>/', views.eliminar_entidad_admin, name='eliminar_entidad_admin'),
    path('mi-panel/usuario/editar/<str:id_usuario>/', views.editar_usuario_admin, name='editar_usuario_admin'),
    path('mi-panel/usuario/eliminar/<str:id_usuario>/', views.eliminar_usuario_admin, name='eliminar_usuario_admin'),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)