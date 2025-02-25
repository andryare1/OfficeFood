from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from .models import User  # Импортируем только вашу модель User
from django.urls import reverse
from django.db import IntegrityError


def home(request):
    # Получаем username из сессии
    username = request.session.get('username')
    return render(request, 'home_auth.html', {'username': username})

def login_view(request):
    error_message = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            # Проверяем существование пользователя и правильность пароля
            user = User.objects.get(username=username, password=password)
            request.session['username'] = username
            return redirect('main:home')
        except User.DoesNotExist:
            error_message = 'Неверный логин или пароль'
            print(f"Authentication failed for username: {username}")
    
    return render(request, 'home_auth.html', {'error_message': error_message})

def register_view(request):
    error_message = None
    if request.method == 'POST':
        username = request.POST.get('new-username')
        password = request.POST.get('new-password')
        confirm_password = request.POST.get('confirm-password')

        try:
            # Проверяем, существует ли пользователь
            if User.objects.filter(username=username).exists():
                error_message = 'Пользователь с таким именем уже существует'
            elif password != confirm_password:
                error_message = 'Пароли не совпадают'
            else:
                # Создаем нового пользователя с ролью 'client' по умолчанию
                user = User.objects.create(
                    username=username,
                    password=password,
                    role='client'
                )
                
                # Сохраняем в сессию
                request.session['username'] = username
                return redirect('main:home')
                
        except Exception as e:
            print(f"Ошибка при регистрации: {str(e)}")
            error_message = f'Ошибка при регистрации: {str(e)}'

    return render(request, 'home_auth.html', {'error_message': error_message})

def logout_view(request):
    if 'username' in request.session:
        del request.session['username']
        messages.success(request, 'Вы успешно вышли из системы')
    return redirect('main:home')

def get_user_profile(request):
    if request.method == 'GET' and 'username' in request.session:
        username = request.session['username']
        try:
            user = User.objects.get(username=username)
            return JsonResponse({
                'username': user.username,
                'role': user.role,
                # Добавьте другие поля, которые хотите показать
            })
        except User.DoesNotExist:
            return JsonResponse({'error': 'Пользователь не найден'}, status=404)
    return JsonResponse({'error': 'Unauthorized'}, status=401)


