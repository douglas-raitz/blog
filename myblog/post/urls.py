from django.urls import path
from . import views

urlpatterns = [
    path('', views.post, name='post'),
    path('<int:post_id>', views.view_post, name='view_post'),
    path('criar/', views.post_create, name='post_create'),
    path('editar/<int:post_id>', views.post_update, name='post_update'),
    path('deletar/<int:post_id>', views.post_delete, name='post_delete'),
    path('search', views.search, name='search'),
]