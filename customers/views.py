import json
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from orders.models import Status, Order
from robots.models import Robot


# отправка email
def send_an_email(order):
    # Отправьте уведомление пользователю
    # send_notification(order.customer, "Робот доступен в наличии.")
    order.status = Status.COMPLETED
    try:
        order.full_clean()
        order.save()
    except ValidationError as e:
        return JsonResponse({'error': f"Ошибка валидации: {str(e)}"}, status=400)
    else:
        return JsonResponse({'message': 'Отправка email'}, status=201)


# изменить статус на ожидание
def change_status_to_waiting(order):
    order.status = Status.WAITING
    try:
        order.full_clean()
        order.save()
    except ValidationError as e:
        return JsonResponse({'error': f"Ошибка валидации: {str(e)}"}, status=400)
    else:
        return JsonResponse({'message': 'Статус заказ изменён на "Ожидание"'}, status=201)


# проверка наличия робота
def check_robot_available(order):
    try:
        robot = Robot.objects.get(serial=order.robot_serial)
        if robot.is_available:
            return send_an_email(order)
        else:
            return change_status_to_waiting(order)
    except Robot.DoesNotExist as e:
        return JsonResponse({'error': f'Робот не найден. Ошибка: {e}'}, status=400)


# создание заказа
def create_order(data):
    order = Order()
    try:
        order.customer_id = data.get('customer_id')
        order.robot_serial = data.get('robot_serial')
        order.order_date = data.get('order_date')
    except KeyError as e:
        return JsonResponse({'error': f'В данных JSON отсутствует ключ: {e}'}, status=400)
    else:
        check_robot_available(order)
        return check_robot_available(order)


# обработка заказа
@csrf_exempt
def process_order(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Ошибка в формате JSON'}, status=400)
        else:
            return create_order(data=data)
    else:
        return JsonResponse({'error': 'Метод не поддерживается'}, status=405)
