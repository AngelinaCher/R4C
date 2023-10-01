from django.urls import path
from . import views

urlpatterns = [
    path('get-report/', views.render_report_page, name='get-report'),  # страница для формирования отчёта
    path('generate_report/', views.generate_report, name='generate_report'),  # сформировать отчёт
    path('api/v1/process-order/', views.process_order, name='process-order'),  # обработать заказ
]
