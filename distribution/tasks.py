from notifications.celery import app
import requests
import datetime
import os
import logging
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpRequest
from .models import Message

#задача для отправки сообщения клиенту через сервис уведомлений
@app.task(name='send_message_to_client')
def send_message(id_message):
    message = Message.objects.get(id=id_message)
    URL = f'https://probe.fbrq.cloud/v1/send/{message.id}'
    #формируем заголовки запроса
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {os.environ.get("TOKEN")}',
        'Content-Type': 'application/json'
    }
    #формируем тело запроса
    request_body = {
        'id': message.id,
        'phone': message.client.phone_number,
        'text': message.distribution.message_text
    }
    #настраиваем логирование
    logging.basicConfig(level=Warning, filename='sending_messages.log',
                        format="%(asctime)s %(levelname)s %(message)s")
    
    text = f'Сообщение клиента с номером {message.client.phone_number} не может быть доставлено. '
    
    try:
        #пытаемся отправить запрос сервису уведомлений
        response = requests.post(
            url=URL,
            headers=headers,
            json=request_body,
            timeout=5
        )
        response.raise_for_status()

    #если он недоступен или долго отвечает
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as er:
        #и если через 20 минут рассылка еще не закончится
        if datetime.datetime.now() + datetime.timedelta(minutes=10) < message.distribution.timestamp_end:
            #то назначаем повторную попытку отправки уведомления через (условно) 10 минут
            send_message.apply_async((message.id,), countdown=1200)
        else:
            #иначе, логируем неудачную попытку связи с сервисом рассылок
            logging.warning(text + f'Ошибка: {er}')

    #если какая-то иная ошибка с запросом
    except requests.exceptions.RequestException as e:
        logging.warning(f'Ошибка запроса: {e}')
        
    #если возникает ошибка, не связанная с запросом
    except Exception as e:
        logging.warning(f'Ошибка: {e}')

    else:
        #если сервис уведомлений ответил некорректными данными
        if response.json() != {"code": 0, "message": 'OK'}:
            logging.info(f'Некорректные данные ответа')
        else:
            #иначе, запрос является успешным, поэтому меняем статус сообщения на "отправлено"
            message.status = 'sent'
            message.save()

#задача для ежедневной отправки статистики по email
@app.task(name='send_statistic_to_email')
def sending_statistic():
    from .views import StatisticViewSet
    #функция для формирования запроса
    def create_request():
        request = HttpRequest()
        request.path = '/api/statistic/'
        request.method = 'GET'
        request.META['HTTP_HOST'] = '127.0.0.1:8000'
        request.META['SERVER_PORT'] = '8000'
        return request

    #формируем данные для отправки сообщения
    view = StatisticViewSet.as_view({'get': 'list'})
    request = create_request()
    response = view(request=request)

    #отправка статистики на email (адрес получателя указан условно)
    send_mail('Статистика по обработанным рассылкам', response.data, settings.EMAIL_HOST_USER, ['to@example.com'])