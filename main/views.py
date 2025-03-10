from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from .models import User  # Импортируем только вашу модель User
from django.urls import reverse
import json

from .models import Dish
from .statistics import generate_dish_category_statistics, export_statistics_to_csv, get_detailed_order_statistics, get_product_usage_statistics, export_product_usage_to_csv
from datetime import datetime

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

def menu(request):
    context = {}
    if request.user.is_authenticated:
        context['username'] = request.user.username
    
    # Получаем все блюда из базы данных
    dishes = Dish.objects.all()
    
    # Группируем блюда по категориям
    categories = {
        'first': {'name': 'Первые блюда', 'dishes': []},
        'second': {'name': 'Вторые блюда', 'dishes': []},
        'drinks': {'name': 'Напитки', 'dishes': []},
        'desserts': {'name': 'Десерты', 'dishes': []},
        'bakery': {'name': 'Выпечка', 'dishes': []},
        'salad': {'name': 'Салаты', 'dishes': []},
    }
    
    for dish in dishes:
        if dish.category in categories:
            categories[dish.category]['dishes'].append(dish)
    
    context['categories'] = categories
    return render(request, 'menu.html', context)

def export_statistics(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    if start_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    if end_date:
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    
    # Получаем статистику
    statistics = generate_dish_category_statistics(start_date, end_date)
    
    # Экспортируем в CSV
    filename = export_statistics_to_csv(statistics)
    
    with open(filename, 'rb') as f:
        response = HttpResponse(f.read(), content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response


import json
from django.shortcuts import render

def product_statistics(request):
    """
    Отображает страницу со статистикой использования продуктов и категорий блюд
    """
    try:
        # Статистика продуктов
        product_stats = get_product_usage_statistics()
        print("\n[DEBUG] Product Stats Raw Data:", product_stats)  # Отладочный вывод

        # Статистика по категориям
        category_stats = generate_dish_category_statistics()
        print("\n[DEBUG] Category Stats Raw Data:", category_stats)  # Отладочный вывод
        
        # Подготавливаем данные для графика продуктов
        chart_data = {
            'names': [stat['product__name'] for stat in product_stats],
            'dishCounts': [stat['dishes_count'] for stat in product_stats],
            'totalCosts': [float(stat['total_cost']) for stat in product_stats]
        }
        print("\n[DEBUG] Chart Data Prepared:", chart_data)  # Отладочный вывод
        
        # Подготавливаем данные для графика категорий
        category_chart_data = {
            'names': [stat['category'] for stat in category_stats],
            'orders': [stat['total_orders'] for stat in category_stats],
            'revenue': [float(stat['total_revenue']) for stat in category_stats],
            'average': [float(stat['average_check']) for stat in category_stats]
        }
        print("\n[DEBUG] Category Chart Data Prepared:", category_chart_data)  # Отладочный вывод
        
        # Проверяем, что данные не пустые
        if not chart_data['names']:
            print("\n[WARNING] Product chart data is empty!")
        if not category_chart_data['names']:
            print("\n[WARNING] Category chart data is empty!")

        context = {
            'statistics': product_stats,
            'category_statistics': category_stats,
            'chart_data': json.dumps(chart_data),
            'category_chart_data': json.dumps(category_chart_data)
        }
        
        print("\n[DEBUG] Final context data:", context)  # Проверка перед передачей в шаблон
        
        return render(request, 'product_statistics.html', context)
        
    except Exception as e:
        print("\n[ERROR] Error in product_statistics view:", str(e))
        # В случае ошибки возвращаем тестовые данные
        test_chart_data = {
            'names': ['Продукт 1', 'Продукт 2', 'Продукт 3'],
            'dishCounts': [5, 3, 7],
            'totalCosts': [1000, 750, 1500]
        }
        
        test_category_data = {
            'names': ['Первые блюда', 'Вторые блюда', 'Напитки'],
            'orders': [10, 15, 8],
            'revenue': [5000, 7500, 2400],
            'average': [500, 500, 300]
        }
        
        return render(request, 'product_statistics.html', {
            'statistics': [],
            'category_statistics': [],
            'chart_data': json.dumps(test_chart_data),
            'category_chart_data': json.dumps(test_category_data)
        })



def export_product_statistics(request):

    statistics = get_product_usage_statistics()
    filename = export_product_usage_to_csv(statistics)
    
    with open(filename, 'rb') as f:
        response = HttpResponse(f.read(), content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response


