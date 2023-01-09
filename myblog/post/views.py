from django.shortcuts import render
from accounts.models import Post

# Create your views here.
def post(request):
    post = Post.objects.all()
    return render(request, 'post/post.html',{
        'posts': post
    })

def view_post(request,post_id):
    post = Post.objects.get(id=post_id)
    return render(request, 'post/view_post.html',{
        'post': post
    })
