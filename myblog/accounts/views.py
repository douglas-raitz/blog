from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Usuario

# Create your views here.
def login(request):
    if request.method != 'POST':
        return render(request, 'accounts/login.html')
    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')

    user = auth.authenticate(request, username=usuario, password=senha)

    if not user:
        return render(request, 'accounts/login.html')
    else:
        auth.login(request, user)
        return redirect('dashboard')

def ver_usuario(request, usuario_id):
    usuario = Usuario.objects.get(id=usuario_id)
    return render(request, 'accounts/ver_usuario.html',{
        'usuario': usuario
    })

def logout(request):
    auth.logout(request)
    return redirect('login')

@login_required(redirect_field_name='login')
def dashboard(request):
    usuarios = Usuario.objects.all()
    return render(request, 'accounts/dashboard.html',{
        'usuario': usuarios
    })