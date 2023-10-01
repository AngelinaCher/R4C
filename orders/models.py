from django.db import models
from customers.models import Customer


class Status(models.TextChoices):
    """ Статус заказа """
    PROCESSING = 'PR', 'В обработке'
    WAITING = 'WT', 'Ожидание'
    COMPLETED = 'CM', 'Выполнен'


class Order(models.Model):
    """ Модель заказа """
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    robot_serial = models.CharField(max_length=5, blank=False, null=False)
    order_date = models.DateField()
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.PROCESSING)
