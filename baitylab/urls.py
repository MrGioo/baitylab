from django.contrib import admin
from django.urls import path, include
from baityapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inicio, name='inicio'),
    path('galeria/', views.galeria, name='galeria'),      
    path('formulario/', views.formulario, name='formulario'),
]
