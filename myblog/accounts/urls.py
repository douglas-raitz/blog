from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('<int:usuario_id>', views.ver_usuario, name='ver_usuario'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('logout', views.logout, name='logout'),

]