from django.urls import path
from . import views

urlpatterns = [
    path('', views.post, name='post'),
    path('<int:post_id>', views.view_post, name='view_post'),
]