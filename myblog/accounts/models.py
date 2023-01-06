from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
# class Usuario(models.Model):
class Categoria(models.Model):
    nome_categoria = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nome_categoria

class Usuario(models.Model):
    nome_autor = models.CharField(max_length=100)
    sobrenome = models.CharField(max_length=100, blank=True)
    data_nascimento = models.DateField(blank=True, null=True)
    date_create = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nome_autor

class Post(models.Model):
    categoria = models.OneToOneField(Categoria, on_delete=models.DO_NOTHING)
    autor = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING)
    titulo = models.CharField(max_length=255)
    publicacao = models.CharField(max_length=1000)
    date_create = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.titulo