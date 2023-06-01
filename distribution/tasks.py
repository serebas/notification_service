from notifications.celery import app
import requests
import os
import logging
from .models import Message

@app.task(name='send_message_to_client')
def send_message(id_message):
    message = Message.objects.get(id=id_message)
    URL = f'https://probe.fbrq.cloud/v1/send/{message.id}'
    
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {os.environ.get("TOKEN")}',
        'Content-Type': 'application/json'
    }
    
    request_body = {
        'id': message.id,
        'phone': message.client.phone_number,
        'text': message.distribution.message_text
    }
    
    logging.basicConfig(level=Warning, filename='sending_messages.log',
                        format="%(asctime)s %(levelname)s %(message)s")
    
    text = f'Сообщение клиента с номером {message.client.phone_number} не может быть доставлено'
    
    try:
        response = requests.post(
            url=URL,
            headers=headers,
            json=request_body,
            timeout=5
        )
        response.raise_for_status()
    except requests.exceptions.Timeout:
        logging.warning('Сервис отправки сообщений долго отвечает. ' + text)
    except requests.exceptions.ConnectionError:
        logging.error('Сервис отправки сообщений не отвечает. ' + text)
    except requests.exceptions.RequestException as e:
        logging.warning(f'Ошибка запроса: {e}')
    except Exception as e:
        logging.warning(f'Ошибка: {e}')
    else:
        if response.json() != {"code": 0, "message": 'OK'}:
            logging.info(f'Некорректные данные ответа')
        else:
            message.status = 'sent'
            message.save()     