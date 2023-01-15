from django.shortcuts import render, redirect
from accounts.models import Post, Categoria, Usuario
from accounts.views import login
from django.core.paginator import Paginator


# Create your views here.
def post(request):
    usuario_id = request.session['usuario_id']
    usuario_name = request.session['usuario_name']
    usuario_tipo = request.session['usuario_tipo']
    
    post = Post.objects.order_by('-date_create')
    
    paginator = Paginator(post,10)

    page_number = request.GET.get('page')
    post = paginator.get_page(page_number)
    
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

    usuario_id = request.session['usuario_id']
    usuario_name = request.session['usuario_name']
    usuario_tipo = request.session['usuario_tipo']

    categoria_name = request.POST.get('categoria')
    titulo = request.POST.get('titulo')
    publicacao = request.POST.get('publicacao')
    
    if usuario_tipo != 'AU':
        return redirect('post')
    
    try:
        if request.method == 'POST':
            if not categoria_name or not titulo or not publicacao:
                return redirect('post_create')

            categoria = Categoria.objects.filter(nome_categoria=categoria_name).first()
            autor = Usuario.objects.filter(id=usuario_id).first()
            post = Post(categoria=categoria,autor=autor,titulo=titulo,publicacao=publicacao)
            post.save()
            return redirect('post')
    except:
        return redirect('post')
    
    return render(request, 'post/post_create.html',{
        'categorias': categorias,
        'usuario_name': usuario_name
    })

def post_update(request,post_id):
    id_post = Post.objects.filter(id=post_id).first()
    categorias = Categoria.objects.all()

    usuario_tipo = request.session['usuario_tipo']

    if usuario_tipo != 'AU':
        return redirect('post')
    
    if request.method == 'POST':
        try:
            categoria_name = request.POST.get('categoria')
            categoria = Categoria.objects.filter(nome_categoria=categoria_name).first()

            id_post.categoria = categoria
            id_post.titulo = request.POST.get('titulo')
            id_post.publicacao = request.POST.get('publicacao')
            id_post.save(update_fields=['categoria','titulo','publicacao'])
            return redirect('post')
        except:
            print('Algo deu errado')
            return redirect('post')

    return render(request, 'post/post_update.html',{
        'id_post':id_post,
        'categorias':categorias,
    })

def post_delete(request,post_id):
    usuario_tipo = request.session['usuario_tipo']

    if usuario_tipo != 'AU':
        return redirect('post')

    id_post = Post.objects.get(id=post_id)
    id_post.delete()
    print('Deletou um usuario com sucesso!')
    return redirect('post')