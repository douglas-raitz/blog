from django.shortcuts import render, redirect
from accounts.models import Post, Categoria, Usuario, Comentario
from accounts.views import login
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q


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
    comentarios = Comentario.objects.all()
    
    usuario_id = request.session['usuario_id']

    if request.method == 'POST':
        usuario = Usuario.objects.get(id=usuario_id)
        comentario = request.POST.get('comentario')
        
        if not comentario:
            messages.add_message(request, messages.ERROR, 'Você precisa ter um comentário para conseguir comentar.')
            return render(request, 'post/view_post.html',{
                'post': post,
                'comentarios':comentarios,
                'usuario_id':usuario_id,
            })

        comentario_save = Comentario(comentario=comentario,usuario=usuario,post=post)
        comentario_save.save()

    return render(request, 'post/view_post.html',{
        'post': post,
        'comentarios':comentarios,
        'usuario_id':usuario_id,
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
                messages.add_message(request, messages.ERROR, 'Todos os campos precisam ser preenchidos.')
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
        'usuario_name': usuario_name,
        'usuario_id': usuario_id,
    })

def post_update(request,post_id):
    id_post = Post.objects.filter(id=post_id).first()
    categorias = Categoria.objects.all()

    usuario_tipo = request.session['usuario_tipo']
    usuario_id = request.session['usuario_id']

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
        'usuario_id':usuario_id,
    })

def post_delete(request,post_id):
    usuario_tipo = request.session['usuario_tipo']

    if usuario_tipo != 'AU':
        return redirect('post')

    id_post = Post.objects.get(id=post_id)
    id_post.delete()
    print('Deletou um usuario com sucesso!')
    return redirect('post')

def search(request):
    usuario_id = request.session['usuario_id']
    usuario_tipo = request.session['usuario_tipo']
    termo = request.GET.get('termo')

    if not termo:
        messages.add_message(request, messages.ERROR, 'O campo de pesquisa não pode ser vazio.')
        return redirect('post')
        
    posts = Post.objects.order_by('-date_create').filter(Q(titulo__icontains=termo))
    
    if not posts:
        messages.add_message(request, messages.ERROR, 'Não contém nenhuma publicação com este titulo.')
        return redirect('post')

    return render(request, 'post/search.html',{
        'posts':posts,
        'usuario_id':usuario_id,
        'usuario_tipo':usuario_tipo,
    })