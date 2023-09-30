from django.db.models.signals import post_save
from django.dispatch import receiver

from orders.models import Order, Status
from robots.models import Robot
from utils.send_notification import send_notification


@receiver(post_save, sender=Robot)
def notify_customer(sender, instance, created, **kwargs) -> None:
    if created:
        waiting_orders = Order.objects.filter(robot_serial=instance.serial, status=Status.WAITING)
        for order in waiting_orders:
            send_notification(customer=order.customer.email, robot_serial=order.robot_serial)
            print('Сообщение отправилось')
            order.status = Status.COMPLETED
            order.save()
