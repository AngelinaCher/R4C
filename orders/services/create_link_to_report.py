import os
from datetime import datetime, timedelta
from django.db.models import Count
from orders.models import Order, Status
from utils.excel_generator import Report


def _get_report_path() -> str:
    """ Формирование отчёта и пути к нему """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    robot_series_data = (Order.objects.filter(order_date__range=(start_date, end_date), status=Status.COMPLETED)
                         .values('robot_serial')
                         .annotate(count=Count('robot_serial'))
                         .order_by('robot_serial'))
    report = Report(list(robot_series_data), start_date, end_date)
    report_path = report.get_path_with_report()
    return report_path


def send_link(request) -> dict:
    """ Отправление ссылки и ответа """
    report_path = _get_report_path()
    report_url = '/media/' + os.path.basename(report_path)
    response_data = {
        'message': 'Сформированный отчёт',
        'download_url': request.build_absolute_uri(report_url)
    }
    return response_data
