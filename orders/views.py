import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from orders.services.create_link_to_report import send_link
from orders.services.create_order import create_order


# получение прямой ссылки на скачивание отчёта
def generate_report(request) -> JsonResponse:
    if request.method == 'POST':
        response_data = send_link(request)
        return JsonResponse(response_data, status=201)
    else:
        return JsonResponse({'error': 'Метод не поддерживается'}, status=405)


# рендер страницы с отчётом
def render_report_page(request):
    return render(request, template_name='orders/report_excel.html')


# обработка заказа
@csrf_exempt
def process_order(request) -> JsonResponse:
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Ошибка в формате JSON'}, status=400)
        else:
            return create_order(data=data)
    else:
        return JsonResponse({'error': 'Метод не поддерживается'}, status=405)
