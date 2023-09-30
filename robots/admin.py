from django.contrib import admin
from .models import Robot


@admin.register(Robot)
class RobotAdmin(admin.ModelAdmin):
    """ Регистрация модели Робот """
    list_display = ['serial', 'is_available']
