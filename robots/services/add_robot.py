from django.http import JsonResponse
from django.core.exceptions import ValidationError
from robots.models import Robot


# валидация данных
def validate_json_data(data: dict) -> JsonResponse | None:
    required_keys = {'model', 'version', 'created'}
    if not set(data.keys()) == required_keys:
        return JsonResponse({'error': 'Неверные ключи в данных JSON.'}, status=400)
    if any(value == '' for value in data.values()):
        return JsonResponse({'error': 'Пустые значения в данных JSON'}, status=400)
    return None


def create_robot(data: dict) -> JsonResponse:
    robot = Robot()
    try:
        robot.serial = f"{data.get('model')}-{data.get('version')}"
        robot.model = str(data.get('model'))
        robot.version = str(data.get('version'))
        robot.created = str(data.get('created'))
    except KeyError as e:
        return JsonResponse({'error': f'В данных JSON отсутствует ключ: {e}'}, status=400)
    try:
        robot.full_clean()
        robot.save()
    except ValidationError as e:
        return JsonResponse({'error': f"Ошибка валидации: {str(e)}"}, status=400)
    else:
        return JsonResponse({'message': 'Запись успешно создана'}, status=201)
