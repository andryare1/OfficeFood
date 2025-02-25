from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Вы успешно вошли в систему!')
            return redirect('home')  # Замените на нужный URL
        else:
            messages.error(request, 'Неверный логин или пароль')
    
    return redirect('home')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('new-username')
        email = request.POST.get('email')
        password = request.POST.get('new-password')
        password_confirm = request.POST.get('confirm-password')
        
        if password != password_confirm:
            messages.error(request, 'Пароли не совпадают')
            return redirect('home')
            
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Пользователь с таким именем уже существует')
            return redirect('home')
            
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Пользователь с таким email уже существует')
            return redirect('home')
            
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            messages.success(request, 'Регистрация успешна!')
            return redirect('home')  # Замените на нужный URL
        except Exception as e:
            messages.error(request, 'Ошибка при регистрации')
            
    return redirect('home') 