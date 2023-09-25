from django.urls import path
from . import views

urlpatterns = [
    path('api/v1/create-robot-record/', views.create_robot_record, name='create_robot_record')
]
