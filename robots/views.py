import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from robots.services.add_robot import validate_json_data, create_robot


@csrf_exempt
def create_robot_record(request) -> JsonResponse:
    """ Обработка запроса на добавление записи в таблицу Робот """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Ошибка в формате JSON'}, status=400)

        validation_error_response = validate_json_data(data)
        if validation_error_response:
            return validation_error_response
        return create_robot(data)
    else:
        return JsonResponse({'error': 'Метод не поддерживается'}, status=405)
