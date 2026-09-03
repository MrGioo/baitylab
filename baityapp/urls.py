from django.contrib import admin
from django.urls import path, include
from baityapp import views

urlpatterns = [
    path('inicio/', views.inicio),
    path('galeria/', views.galeria),
    path('formulario/', views.formulario),
]
