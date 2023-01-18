from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('<int:usuario_id>', views.ver_usuario, name='ver_usuario'),
    path('logout', views.logout, name='logout'),
    path('cadastro', views.cadastro, name='cadastro'),
    path('cadastrar', views.cadastrar, name='cadastrar'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('usuarios', views.usuarios, name='usuarios'),
    path('categorias', views.categorias, name='categorias'),
    path('categoria', views.categoria, name='categoria'),

]