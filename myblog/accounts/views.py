from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User, Permission
from django.contrib.auth.decorators import login_required
from .models import Usuario, Categoria
from django.contrib import messages
from django.core.paginator import Paginator


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
        request.session['usuario_id'] = user.id
        request.session['usuario_name'] = user.nome_autor
        request.session['usuario_tipo'] = user.tipo

        usuario_id = request.session['usuario_id']
        usuario_name = request.session['usuario_name']
        usuario_tipo = request.session['usuario_tipo']
        
        return render(request, 'accounts/dashboard.html', {
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
    return render(request, 'accounts/ver_usuario.html',{
        'usuario': usuario
    })

def logout(request):
    auth.logout(request)
    return redirect('login')


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
