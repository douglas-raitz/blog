from django.shortcuts import render, redirect
from accounts.models import Post, Categoria, Usuario
from accounts.views import login

# Create your views here.
def post(request):
    usuario_id = request.session['usuario_id']
    usuario_name = request.session['usuario_name']
    usuario_tipo = request.session['usuario_tipo']
    
    post = Post.objects.all()
    return render(request, 'post/post.html',{
        'posts': post,
        'usuario_id':usuario_id,
        'usuario_name':usuario_name,
        'usuario_tipo':usuario_tipo,
    })

def view_post(request,post_id):
    post = Post.objects.get(id=post_id)
    return render(request, 'post/view_post.html',{
        'post': post
    })

def post_create(request):
    categorias = Categoria.objects.all()

    # usuario_id = request.session['usuario_id']
    usuario_name = request.session['usuario_name']
    usuario_tipo = request.session['usuario_tipo']

    categoria_name = request.POST.get('categoria')
    autor_nome = request.POST.get(usuario_name)
    titulo = request.POST.get('titulo')
    publicacao = request.POST.get('publicacao')

    if usuario_tipo != 'AU':
        return redirect('post')
    
    if request.method == 'POST':
        categoria = Categoria.objects.filter(nome_categoria=categoria_name).first()
        autor = Usuario.objects.filter(nome_autor=autor_nome).first()
        post = Post(categoria=categoria,autor=autor,titulo=titulo,publicacao=publicacao)
        post.save()
        return render(request, 'post/post_create.html')
    
    return render(request, 'post/post_create.html',{
        'categorias': categorias,
        'usuario_name': usuario_name
    })