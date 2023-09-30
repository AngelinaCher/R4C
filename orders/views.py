import os
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Count
from .models import Order, Status
from .report_generator.excel_generator import get_report


# формирование отчёт
def generate_report(request):
    if request.method == 'POST':
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        robot_series_data = (Order.objects.filter(order_date__range=(start_date, end_date), status=Status.COMPLETED)
                             .values('robot_serial')
                             .annotate(count=Count('robot_serial'))
                             .order_by('robot_serial'))
        report_path = get_report(list(robot_series_data), start_date, end_date)
        report_url = '/media/' + os.path.basename(report_path)
        response_data = {
            'message': 'Сформированный отчёт',
            'download_url': request.build_absolute_uri(report_url)
        }
        return JsonResponse(response_data, status=201)
    else:
        return JsonResponse({'error': 'Метод не поддерживается'}, status=405)


# рендер страницы
def render_report_page(request):
    return render(request, template_name='orders/report_excel.html')
