from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    role = models.CharField(max_length=50)  # 'manager', 'dispatcher', 'calculator', 'client'

    def __str__(self):
        return self.username


class Client(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    order_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order #{self.id} for {self.client.name}"


class Menu(models.Model):
    menu_type = models.CharField(max_length=50)  # 'day' or 'week'
    menu_date_start = models.DateField()
    menu_date_end = models.DateField()

    def __str__(self):
        return f"{self.menu_type} Menu from {self.menu_date_start} to {self.menu_date_end}"


class Dish(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
     image = models.ImageField(
        upload_to='dishes/',
        storage=FileSystemStorage(location=settings.MEDIA_ROOT),
        blank=True, 
        null=True
    )

    def __str__(self):
        return self.name


class MenuDish(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.dish.name} in {self.menu.menu_type} menu"


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.dish.name} for Order #{self.order.id}"


class Product(models.Model):
    name = models.CharField(max_length=255)
    unit = models.CharField(max_length=50)  # e.g., kg, liters
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class DishProduct(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_needed = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity_needed} of {self.product.name} for {self.dish.name}"
