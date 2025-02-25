from django.contrib import admin
from .models import User, Client, Order, Menu, Dish, MenuDish, OrderDetail, Product, DishProduct

admin.site.register(User)
admin.site.register(Client)
admin.site.register(Order)
admin.site.register(Menu)
admin.site.register(Dish)
admin.site.register(MenuDish)
admin.site.register(OrderDetail)
admin.site.register(Product)
admin.site.register(DishProduct)
