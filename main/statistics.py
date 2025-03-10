from django.db.models import Sum, Count, F
from django.db import models
import csv
from datetime import datetime
from .models import Order, OrderDetail, Dish, DishProduct, Product

def generate_dish_category_statistics(start_date=None, end_date=None):
    """
    Генерирует статистику по категориям блюд:
    - Количество заказов по категориям
    - Общая выручка по категориям
    - Средний чек заказа с блюдами каждой категории
    """
    query = OrderDetail.objects.select_related('dish', 'order').annotate(
        category=F('dish__category'),
        total_amount=F('quantity') * F('price')
    )
    
    if start_date:
        query = query.filter(order__order_date__gte=start_date)
    if end_date:
        query = query.filter(order__order_date__lte=end_date)

    statistics = query.values('category').annotate(
        total_orders=Count('order', distinct=True),
        total_revenue=Sum('total_amount'),
        total_dishes_sold=Sum('quantity')
    ).annotate(
        average_check=F('total_revenue') / F('total_orders')
    )

    return statistics

def export_statistics_to_csv(statistics, filename=None):
    """
    Экспортирует статистику в CSV файл
    """
    if not filename:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'dish_statistics_{timestamp}.csv'

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['category', 'total_orders', 'total_revenue', 
                     'total_dishes_sold', 'average_check']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for stat in statistics:
            writer.writerow(stat)
    
    return filename

def get_detailed_order_statistics():
    """
    Получает детальную статистику по заказам с группировкой по клиентам и категориям блюд
    """
    return OrderDetail.objects.select_related(
        'order__client', 'dish'
    ).values(
        'order__client__name',
        'dish__category'
    ).annotate(
        total_spent=Sum(F('quantity') * F('price')),
        orders_count=Count('order', distinct=True),
        dishes_ordered=Count('dish')
    ).order_by('-total_spent')

def get_product_usage_statistics():
    """
    Получает статистику использования продуктов:
    - Количество блюд, в которых используется продукт
    - Общее количество использованного продукта
    - Общая стоимость использования продукта
    """
    return DishProduct.objects.select_related('product', 'dish').values(
        'product__name',
        'product__unit'
    ).annotate(
        dishes_count=Count('dish', distinct=True),
        total_quantity=Sum('quantity_needed'),
        total_cost=Sum(F('quantity_needed') * F('product__price_per_unit'))
    ).order_by('-total_cost')

def export_product_usage_to_csv(statistics, filename=None):
    """
    Экспортирует статистику использования продуктов в CSV файл
    """
    if not filename:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'product_usage_statistics_{timestamp}.csv'

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['product__name', 'dishes_count', 'total_quantity', 'total_cost', 'product__unit']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for stat in statistics:
            writer.writerow(stat)
    
    return filename 