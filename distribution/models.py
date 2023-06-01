from django.db import models

class Distribution(models.Model):
    message_text = models.CharField(max_length=255)
    filter = models.CharField(max_length=15)
    timestamp_start = models.DateTimeField(null=True)
    timestamp_end = models.DateTimeField(null=True)

    def __str__(self) -> str:
        return f'disctribution for clients with {self.filter}'
    
    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class Client(models.Model):
    import pytz
    TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))

    phone_number = models.CharField(max_length=11, verbose_name='Номер телефона')
    MNC = models.PositiveIntegerField(verbose_name='Код страны')
    TAG = models.SlugField(db_index=True, max_length=15, verbose_name='ТЕГ')
    timezone = models.CharField(max_length=32, choices=TIMEZONES, verbose_name='Часовой пояс') 

    def __str__(self) -> str:
        return self.phone_number
    
    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Message(models.Model):
    STATUS = [
        ('sent', 'sent'),
        ('not sent', 'not sent'),
    ]

    timestamp_create = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=8, choices=STATUS, default='not sent')
    distribution = models.ForeignKey(to=Distribution, null=True, on_delete=models.SET_NULL, verbose_name='Рассылка')
    client = models.ForeignKey(to=Client, null=True, on_delete=models.SET_NULL, verbose_name='Номер клиента')

    def __str__(self) -> str:
        return f'Message {self.id}, {self.status}'
    
    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'