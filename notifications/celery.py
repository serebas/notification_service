import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'notifications.settings')
app = Celery('notifications')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

#создаем расписание задач для отправки статистики по email каждый день в 12:00
app.conf.beat_schedule = {
    'send_every_day': {
        'task': 'send_statistic_to_email',
        'schedule': crontab(minute=0, hour=12),
    },
}