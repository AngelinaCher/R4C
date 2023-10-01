from django.http import JsonResponse
from django.db import transaction
from django.core.exceptions import ValidationError
from utils.send_notification import send_notification
from orders.models import Status, Order
from robots.models import Robot


def _send_an_email(order: Order) -> JsonResponse:
    """ Отправка email сообщение клиента и изменение статус заказа на "Выполнен" """
    send_notification(customer=order.customer.email, robot_serial=order.robot_serial)
    order.status = Status.COMPLETED
    order.full_clean()
    order.save()
    return JsonResponse({'message': 'Письмо отправлено'}, status=201)


def _change_status_to_waiting(order):
    """ Меняет статус заказа на "Ожидание" """
    order.status = Status.WAITING
    order.full_clean()
    order.save()
    return JsonResponse({'message': 'Статус заказа изменён на "Ожидание"'}, status=201)


def create_order(data: dict) -> JsonResponse:
    """ Добавление заказа в БД и его обработка """
    order = Order(customer_id=data.get('customer_id'),
                  robot_serial=data.get('robot_serial'),
                  order_date=data.get('order_date'),
                  status=Status.PROCESSING)
    try:
        with transaction.atomic():
            robot = Robot.objects.get(serial=order.robot_serial)
        if robot:
            return _send_an_email(order)
    except Robot.DoesNotExist:
        return _change_status_to_waiting(order)
    except ValidationError as e:
        return JsonResponse({'error': f"Ошибка валидации: {str(e)}"}, status=400)


