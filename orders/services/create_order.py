from django.http import JsonResponse
from django.db import transaction
from django.core.exceptions import ValidationError
from utils.send_notification import send_notification
from orders.models import Status, Order
from robots.models import Robot


# отправка email
def send_an_email(order: Order) -> JsonResponse:
    send_notification(customer=order.customer.email, robot_serial=order.robot_serial)
    order.status = Status.COMPLETED
    order.full_clean()
    order.save()
    return JsonResponse({'message': 'Письмо отправлено'}, status=201)


# изменить статус на ожидание
def change_status_to_waiting(order):
    order.status = Status.WAITING
    order.full_clean()
    order.save()
    return JsonResponse({'message': 'Статус заказа изменён на "Ожидание"'}, status=201)


# создание заказа
def create_order(data: dict) -> JsonResponse:
    order = Order(customer_id=data.get('customer_id'),
                  robot_serial=data.get('robot_serial'),
                  order_date=data.get('order_date'),
                  status=Status.PROCESSING)
    try:
        with transaction.atomic():
            robot = Robot.objects.get(serial=order.robot_serial)
        if robot:
            return send_an_email(order)
    except Robot.DoesNotExist:
        return change_status_to_waiting(order)
    except ValidationError as e:
        return JsonResponse({'error': f"Ошибка валидации: {str(e)}"}, status=400)


