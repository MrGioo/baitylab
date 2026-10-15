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
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)