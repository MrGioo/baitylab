from django.db import models

# Create your models here.


class UsuarioSteam(models.Model):
    id_usuario = models.CharField(max_length=10, primary_key=True) 
    nick_steam = models.CharField(max_length=100) 
    correo = models.EmailField() 

    def __str__(self):
        return self.nick_steam

class EntidadVertedero(models.Model):
    id_entidad = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50) 
    categoria = models.CharField(max_length=50)
    descripcion = models.TextField()
    # NUEVO CAMPO PARA LA IMAGEN:
    imagen = models.ImageField(upload_to='entidades/', null=True, blank=True)

    def __str__(self):
        return self.nombre

class ReporteQueja(models.Model):
    id = models.AutoField(primary_key=True) 
    usuario = models.ForeignKey(UsuarioSteam, on_delete=models.CASCADE)
    entidad_involucrada = models.ForeignKey(EntidadVertedero, on_delete=models.CASCADE)
    tipo_estafa = models.CharField(max_length=50) 
    mensaje = models.TextField() 
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Queja {self.id} de {self.usuario.nick_steam}"