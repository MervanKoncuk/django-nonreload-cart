from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# Create your views here.
def userRegister(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    context = {
        'form':form
    }
    return render(request, 'register.html', context)

def userLogin(request):
    if request.method == 'POST':
        kullanici = request.POST['kullanici']
        sifre = request.POST['sifre']

        user = authenticate(request, username = kullanici, password = sifre)

        if user is not None:
            login(request, user)
            messages.success(request, 'Giriş yapıldı')
            return redirect('index')
        else:
            messages.error(request, 'Kullanıcı adı veya şifre hatalı')
            return redirect('login')
    return render(request, 'login.html')

def userLogout(request):
    logout(request)
    messages.success(request, 'Çıkış yapıldı')
    return redirect('index')

def change(request):
    user = request.user
    if request.method == 'POST':
        eski = request.POST['eski']
        yeni = request.POST['yeni']

        degis = authenticate(request, username = user, password = eski)
        if degis is not None:
            user.set_password(yeni)
            user.save()
            messages.success(request, 'Şifre güncellendi')
            return redirect('login')
        else:
            messages.error(request, 'Şifre hatalı')
            return redirect('change')
    return render(request, 'change.html')