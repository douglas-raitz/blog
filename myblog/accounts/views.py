from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User, Permission
from django.contrib.auth.decorators import login_required
from .models import Usuario, Categoria

# Create your views here.
def login(request):
    if request.method != 'POST':
        return render(request, 'accounts/login.html')
    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')

    user = Usuario.objects.filter(usuario=usuario, senha=senha).first()
    
    request.session['usuario_logado'] = user.id

    if not user:
        return render(request, 'accounts/login.html')
    else:
        user_login = request.session['usuario_logado']
        return render(request, 'accounts/dashboard.html', {
            "user": user,
            "user_login": user_login
        })
    

def cadastro(request):
    if request.method != 'POST':
        return render(request, 'accounts/cadastro.html')
    
    usuario = request.POST.get('usuario')
    nome = request.POST.get('nome')
    sobrenome = request.POST.get('sobrenome')
    data_nascimento = request.POST.get('data_nascimento')
    nivel_acesso = request.POST.get('nivel_acesso')
    senha = request.POST.get('senha')
    senha2 = request.POST.get('senha2')

    if senha != senha2:
        return render(request, 'accounts/cadastro.html')

    if User.objects.filter(username=usuario).exists():
        return render(request, 'accounts/cadastro.html')


    user = Usuario(usuario=usuario,nome_autor=nome,sobrenome=sobrenome,data_nascimento=data_nascimento,tipo=nivel_acesso,senha=senha)
    user.save()
    return redirect('dashboard')
    


def ver_usuario(request, usuario_id):
    usuario = Usuario.objects.get(id=usuario_id)
    return render(request, 'accounts/ver_usuario.html',{
        'usuario': usuario
    })

def logout(request):
    auth.logout(request)
    return redirect('login')


def dashboard(request):
    return render(request, 'accounts/dashboard.html')


def usuarios(request):
    user = Usuario.objects.all()
    user_login = request.session['usuario_logado']
 
    return render(request, 'accounts/usuarios.html',{
        'user': user,
        'user_login': user_login
    })

def categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'accounts/categorias.html', {
        "categorias":categorias
    })

def categoria(request):
    if request.method != 'POST':
        return render(request, 'accounts/categoria.html')

    nome_categoria = request.POST.get('categoria')

    new_categoria = Categoria(nome_categoria=nome_categoria)
    new_categoria.save()
    return redirect('categorias')