from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

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

def logout(request):
    auth.logout(request)
    return redirect('login')

@login_required(redirect_field_name='login')
def dashboard(request):
    return render(request, 'accounts/dashboard.html')