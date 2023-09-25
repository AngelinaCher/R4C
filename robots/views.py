import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from .models import Robot


# Валидация данных
def validate_json_data(data: dict) -> JsonResponse | None:
    required_keys = {'model', 'version', 'created'}
    if not set(data.keys()) == required_keys:
        return JsonResponse({'error': 'Неверные ключи в данных JSON.'}, status=400)
    if any(value == '' for value in data.values()):
        return JsonResponse({'error': 'Пустые значения в данных JSON'}, status=400)
    return None


# добавление записи
@csrf_exempt
def create_robot_record(request) -> JsonResponse:
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Ошибка в формате JSON'}, status=400)

        validation_error_response = validate_json_data(data)
        if validation_error_response:
            return validation_error_response

        robot = Robot()
        try:
            robot.serial = f"{data.get('model')}-{data.get('version')}"
            robot.model = str(data.get('model'))
            robot.version = str(data.get('version'))
            robot.created = str(data.get('created'))
        except KeyError as e:
            return JsonResponse({'error': f'В данных JSON отсутствует ключ: {e}'}, status=400)

        try:
            robot.clean()
            robot.save()
        except ValidationError as e:
            return JsonResponse({'error': f"Ошибка валидации: {str(e)}"}, status=400)
        else:
            return JsonResponse({'message': 'Запись успешно создана'}, status=201)
    else:
        return JsonResponse({'error': 'Метод не поддерживается'}, status=405)
