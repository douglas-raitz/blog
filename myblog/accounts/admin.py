from django.contrib import admin
from .models import Categoria, Usuario, Post

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nome_autor','sobrenome','data_nascimento','date_create')
    list_per_page = 10
    search_fields = ('nome_autor','sobrenome')

class PostAdmin(admin.ModelAdmin):
    list_display = ('titulo','date_create')

admin.site.register(Categoria)
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Post, PostAdmin)