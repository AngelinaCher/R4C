from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """ Регистрация модели заказа """
    list_display = ('customer', 'robot_serial', 'order_date')
