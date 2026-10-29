from django.contrib import admin
from django.urls import path, include
from baityapp import views
from django.conf import settings # NUEVO
from django.conf.urls.static import static # NUEVO

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inicio, name='inicio'),
    path('galeria/', views.galeria, name='galeria'),
    path('formulario/', views.formulario, name='formulario'),
    path('registro/', views.registro, name='registro'), 
    path('accounts/', include('django.contrib.auth.urls')),
]

# NUEVO: Permitir ver las imágenes en modo DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)