from django.urls import path
from . import views
from customers.views import process_order

urlpatterns = [
    path('api/v1/process-order/', views.process_order, name='process-order'),

]
