from django.shortcuts import render
from accounts.models import Post
from accounts.views import login

# Create your views here.
def post(request):
    user_login = request.session['usuario_logado']
    
    post = Post.objects.all()
    return render(request, 'post/post.html',{
        'posts': post,
        'user_login':user_login
    })

def view_post(request,post_id):
    post = Post.objects.get(id=post_id)
    return render(request, 'post/view_post.html',{
        'post': post
    })