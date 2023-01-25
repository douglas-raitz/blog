from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User, Permission
from django.contrib.auth.decorators import login_required
from .models import Usuario, Categoria, Post
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils import timezone


# Create your views here.

def login(request):

    if request.method != 'POST':
        return render(request, 'accounts/login.html')

    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')

    user = Usuario.objects.filter(usuario=usuario, senha=senha).first()

    if not user:
        messages.add_message(request, messages.ERROR, 'OPS, Você precisa ter um usuário cadastrado para ter acesso!.')
        return redirect('login')
    else:
        posts = Post.objects.order_by('-date_create')
        request.session['usuario_id'] = user.id
        request.session['usuario_name'] = user.nome_autor
        request.session['usuario_tipo'] = user.tipo

        usuario_id = request.session['usuario_id']
        usuario_name = request.session['usuario_name']
        usuario_tipo = request.session['usuario_tipo']

        paginator = Paginator(posts,10)

        page_number = request.GET.get('page')
        posts = paginator.get_page(page_number)
        
        return render(request, 'post/post.html', {
            "posts":posts,
            "usuario_id": usuario_id,
            "usuario_name": usuario_name,
            "usuario_tipo": usuario_tipo,
        })
    

def cadastro(request):
    usuario_tipo = request.session['usuario_tipo']
    usuario_id = request.session['usuario_id']
    nivel_acesso = Usuario.objects.all()

    if usuario_tipo != 'AD':
        return redirect('dashboard')

    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        data_nascimento = request.POST.get('data_nascimento')
        nivel_acesso = request.POST.get('nivel_acesso')
        senha = request.POST.get('senha')
        senha2 = request.POST.get('senha2')


        if Usuario.objects.filter(usuario=usuario):
            messages.add_message(request, messages.ERROR, 'Nome de usuário já em uso.')
            return render(request, 'accounts/cadastro.html',{
                'usuario_id':usuario_id,
                'usuario_tipo':usuario_tipo,
            })
        

        if senha != senha2:
            messages.add_message(request, messages.ERROR, 'As senhas precisam ser iguais.')
            return render(request, 'accounts/cadastro.html',{
                'usuario_id':usuario_id,
                'usuario_tipo':usuario_tipo,
            })

        if not usuario or not nome or not sobrenome or not data_nascimento or not nivel_acesso or not senha:
            messages.add_message(request, messages.ERROR, 'Todos os campos precisam ser preenchidos!')
            return render(request, 'accounts/cadastro.html',{
                'usuario_id':usuario_id,
                'usuario_tipo':usuario_tipo,
            })

        try:
            user = Usuario(usuario=usuario,nome_autor=nome,sobrenome=sobrenome,data_nascimento=data_nascimento,tipo=nivel_acesso,senha=senha)
            user.save()
            messages.add_message(request, messages.SUCCESS, 'Cadastro concluído com sucesso!')
            return redirect('dashboard')
        except:
            messages.add_message(request, messages.ERROR, 'Não foi possível adicionar um novo usuário!')
            return redirect('dashboard')

    return render(request, 'accounts/cadastro.html',{
        'usuario_id':usuario_id,
        'usuario_tipo':usuario_tipo,
    })


def cadastrar(request):

    if request.method == 'POST':
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        usuario = request.POST.get('usuario')
        data_nascimento = request.POST.get('data_nascimento')
        senha = request.POST.get('senha')
        senha2 = request.POST.get('senha2')
        
        if senha != senha2:
            messages.add_message(request, messages.ERROR, 'As senhas precisam ser iguais.')
            return render(request, 'accounts/cadastro_comum.html')

        if Usuario.objects.filter(usuario=usuario):
            messages.add_message(request, messages.ERROR, 'Nome de usuário já em uso.')
            return render(request, 'accounts/cadastro_comum.html')

        if not nome or not sobrenome or not usuario or not data_nascimento or not senha:
            messages.add_message(request, messages.ERROR, 'Você precisa adicionar todos os campos para concluir seu cadastro!')
            return render(request, 'accounts/cadastro_comum.html')

        try:
            cadastro_comum = Usuario(nome_autor=nome,sobrenome=sobrenome,usuario=usuario,data_nascimento=data_nascimento,senha=senha)
            cadastro_comum.save()
            messages.add_message(request, messages.SUCCESS, 'Cadastro concluido, tudo pronto para você fazer login')
            return redirect('login')
        except:
            return redirect('login')
    
    return render(request, 'accounts/cadastro_comum.html')

def ver_usuario(request, usuario_id):
    usuario = Usuario.objects.get(id=usuario_id)
    usuario_tipo = request.session['usuario_tipo']
    
    if usuario_tipo != 'AD':
        return redirect('post')

    return render(request, 'accounts/ver_usuario.html',{
        'usuario': usuario
    })

def usuario_update(request,usuario_id):
    id_usuario = Usuario.objects.filter(id=usuario_id).first()
    usuario_id = request.session['usuario_id']
    usuario_tipo = request.session['usuario_tipo']

    if usuario_tipo != 'AD':
        return redirect('login')

    if request.method == 'POST':

        try:
            if request.POST.get('senha2') != request.POST.get('senha'):
                messages.add_message(request, messages.ERROR, 'As senhas precisam ser iguais.')
                return redirect('usuario_edit')
                
            id_usuario.nome_autor = request.POST.get('nome')
            id_usuario.sobrenome = request.POST.get('sobrenome')
            id_usuario.usuario = request.POST.get('usuario')
            id_usuario.data_nascimento = request.POST.get('data_nascimento')
            id_usuario.tipo = request.POST.get('nivel_acesso')
            id_usuario.senha = request.POST.get('senha')
            id_usuario.save()
            messages.add_message(request, messages.SUCCESS, 'Usuário editado com sucesso!')
            return redirect('usuarios')
        except:
            messages.add_message(request, messages.ERROR, 'Não foi possível editar este usuário.')
    
    return render(request, 'accounts/usuario_edit.html',{
        'id_usuario':id_usuario,
        'usuario_id': usuario_id,
        'usuario_tipo': usuario_tipo,

    })

def usuario_delete(request,usuario_id):
    usuario_tipo = request.session['usuario_tipo']
    
    if usuario_tipo != 'AD':
        return redirect('post')

    id_usuario = Usuario.objects.get(id=usuario_id)
    try:
        id_usuario.delete()
        messages.add_message(request, messages.SUCCESS, 'Usuário excluído com sucesso!')
        return redirect('usuarios')
    except:
        messages.add_message(request, messages.ERROR, 'Algo deu errado, não foi possível excluir este usuário.')
        return redirect('usuarios')

def dashboard(request):
    usuario_id = request.session['usuario_id']
    usuario_name = request.session['usuario_name']
    usuario_tipo = request.session['usuario_tipo']

    return render(request, 'accounts/dashboard.html',{
        'usuario_id':usuario_id,
        'usuario_name':usuario_name,
        'usuario_tipo':usuario_tipo,
    })


def usuarios(request):
    usuario_id = request.session['usuario_id']
    usuario_name = request.session['usuario_name']
    usuario_tipo = request.session['usuario_tipo']

    if usuario_tipo != 'AD':
        return redirect('dashboard')

    user = Usuario.objects.order_by('nome_autor')
    paginator = Paginator(user, 15)

    num_page = request.GET.get('p')
    user = paginator.get_page(num_page)

    return render(request, 'accounts/usuarios.html',{
        'user':user,
        'usuario_id':usuario_id,
        'usuario_name':usuario_name,
        'usuario_tipo':usuario_tipo,
    })

def categorias(request):
    usuario_id = request.session['usuario_id']
    usuario_name = request.session['usuario_name']
    usuario_tipo = request.session['usuario_tipo']
    
    if usuario_tipo != 'AD':
        return redirect('dashboard')

    categorias = Categoria.objects.all()

    return render(request, 'accounts/categorias.html', {
        "categorias":categorias,
        'usuario_id':usuario_id,
        'usuario_name':usuario_name,
        'usuario_tipo':usuario_tipo,
    })

def categoria(request):
    usuario_tipo = request.session['usuario_tipo']
    usuario_id = request.session['usuario_id']
    if usuario_tipo != 'AD':
        return redirect('dashboard')

    if request.method == 'POST':
        nome_categoria = request.POST.get('categoria')

        if not nome_categoria:
            messages.add_message(request, messages.ERROR, 'Você precisa adicionar o nome da categoria !')
            return render(request, 'accounts/categoria.html',{
                'usuario_tipo':usuario_tipo,
                'usuario_id':usuario_id,
            })

        new_categoria = Categoria(nome_categoria=nome_categoria)
        new_categoria.save()
        return redirect('categorias')
        
    return render(request, 'accounts/categoria.html',{
        'usuario_tipo':usuario_tipo,
        'usuario_id':usuario_id,
    })

def logout(request):
    auth.logout(request)
    return redirect('login')