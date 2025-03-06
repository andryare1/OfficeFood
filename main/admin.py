from django.contrib import admin
from .models import User, Client, Order, Menu, Dish, MenuDish, OrderDetail, Product, DishProduct
from django.utils.html import format_html

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'role']
    search_fields = ['username']
    list_filter = ['role']
    ordering = ['username']

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'address', 'phone']
    search_fields = ['name', 'address', 'phone', 'user__username']
    list_filter = ['user']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['client', 'order_date', 'total_price']
    search_fields = ['client__name']
    list_filter = ['order_date']
    ordering = ['-order_date']

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['menu_type', 'menu_date_start', 'menu_date_end']
    search_fields = ['menu_type']
    list_filter = ['menu_type', 'menu_date_start']
    ordering = ['-menu_date_start']

@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'description', 'display_image']
    search_fields = ['name', 'description']
    list_filter = ['price']
    ordering = ['name']
    readonly_fields = ['preview_image']
    
    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return "Нет изображения"
    
    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="200" height="200" />', obj.image.url)
        return "Нет изображения"
    
    display_image.short_description = 'Изображение'
    preview_image.short_description = 'Предпросмотр изображения'

    fields = ['name', 'price', 'description', 'image', 'preview_image']

@admin.register(MenuDish)
class MenuDishAdmin(admin.ModelAdmin):
    list_display = ['menu', 'dish', 'day_of_week']
    search_fields = ['dish__name', 'day_of_week']
    list_filter = ['menu', 'day_of_week']

@admin.register(OrderDetail)
class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ['order', 'dish', 'quantity', 'price']
    search_fields = ['order__client__name', 'dish__name']
    list_filter = ['order', 'dish']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'unit', 'price_per_unit']
    search_fields = ['name']
    list_filter = ['unit']
    ordering = ['name']

@admin.register(DishProduct)
class DishProductAdmin(admin.ModelAdmin):
    list_display = ['dish', 'product', 'quantity_needed']
    search_fields = ['dish__name', 'product__name']
    list_filter = ['dish', 'product']
