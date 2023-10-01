import os
from dotenv import load_dotenv
from django.http import JsonResponse
from django.core.mail import send_mail

load_dotenv()


def send_notification(customer: str, robot_serial: str) -> None | JsonResponse:
    """ Отправка уведомления о появлении в наличии Робота """
    model, version = robot_serial.split('-')
    email_text = (f"Добрый день!\n"
                  f"Недавно вы интересовались нашим роботом модели {model}, версии {version}.\n"
                  f"Этот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами.")
    subject = 'Уведомление о заказе'
    from_email = os.getenv('EMAIL_HOST_USER')
    recipient_list = [customer]
    try:
        send_mail(subject=subject, message=email_text, from_email=from_email, recipient_list=recipient_list)
    except Exception as e:
        return JsonResponse({'error': f"Ошибка в отправке email {str(e)}"}, status=400)
