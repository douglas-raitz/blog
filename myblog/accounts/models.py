from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.forms import ModelForm

# Create your models here.
# class Usuario(models.Model):
class Categoria(models.Model):
    nome_categoria = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nome_categoria


class Usuario(models.Model):
    choices = [('AD', 'Administrador'), ('AU', 'Autor'),('CO', 'Comum')]
    nome_autor = models.CharField(max_length=100)
    sobrenome = models.CharField(max_length=100, blank=True)
    usuario = models.CharField(max_length=100)
    data_nascimento = models.DateField(blank=True, null=True)
    date_create = models.DateTimeField(default=timezone.now)
    senha = models.CharField(max_length=100)
    tipo = models.CharField(max_length=30, choices=choices, default='CO')

    def __str__(self):
        return self.nome_autor

class Post(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING, related_name='categoria')
    autor = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING)
    titulo = models.CharField(max_length=255)
    publicacao = models.CharField(max_length=1000)
    date_create = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.titulo


class Comentario(models.Model):
    post = models.ForeignKey(Post,on_delete=models.DO_NOTHING)
    usuario = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING)
    comentario = models.CharField(max_length=1000)
    date_create = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.comentario