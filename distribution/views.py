from rest_framework.views import *
from rest_framework import mixins, viewsets
from datetime import datetime
from django.db.models import Q
from django.db.models import Count
from .serializers import ClientSerializer, DisctributionSerializer, MessageSerializer
from .models import Message, Distribution, Client
from .tasks import send_message
import pytz



class ClientViewSet(mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    

class DistributionViewSet(mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):
    
    queryset = Distribution.objects.all()
    serializer_class = DisctributionSerializer

    #создание рассылки
    def create(self, request, *args, **kwargs):
        #сериализуем поступившие данные из запроса и создаем рассылку
        serializer = DisctributionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        distribution = Distribution.objects.create(**serializer.data)

        #выделяем все необходимые атрибуты рассылки (времена начала и конца и фильтр)
        timestamp_start = datetime.strptime(serializer.data['timestamp_start'][:-6], "%Y-%m-%dT%H:%M:%S")
        timestamp_end = datetime.strptime(serializer.data['timestamp_end'][:-6], "%Y-%m-%dT%H:%M:%S")
        filter = serializer.data['filter']

        #отбираем всех клиентов, которые подходят под указанный фильтр
        clients = Client.objects.filter(Q(MNC=filter) | Q(TAG=filter))

        for client in clients:
            #создаем объект сообщения с текущими рассылкой и клиентом
            message = Message.objects.create(distribution=distribution, client=client)

            #узнаем местное время клиента
            client_tz = pytz.timezone(client.timezone)
            client_datetime = datetime.now(client_tz)

            #если местное время клиента больше времени начала, но меньше времени конца рассылки
            if timestamp_start < client_datetime < timestamp_end:

                #рассылаем сообщения сразу           
                send_message.apply_async((message.id,), countdown=0.1)  

            #если время начала рассылки больше местного времени клиента           
            elif timestamp_start > client_datetime:

                #отправляем сообщение после наступления времени начала рассылки                         
                send_message.apply_async((message.id,), eta=timestamp_start) 

        #отправляем клиенту ответ об успешном создании рассылки
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    #получение детальной статистики по запросу
    def retrieve(self, request, *args, **kwargs):
        #выделяем из данных полученного запроса id рассылки
        pk = kwargs.get('pk')

        try:
            #берем из БД все сообщения указанной рассылки которые были отправлены, сериализуем их и отправляем клиенту   
            messages = Message.objects.filter(distribution_id=pk, status='sent')
            serializer = MessageSerializer(messages, many=True)
            return Response(serializer.data)
        except:
            #если в БД нету рассылки с указанным id, отправляем клиенту об этом ответ
            return Response({'detail': 'Указан неверный id'}, status=status.HTTP_204_NO_CONTENT)
    

class StatisticViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    #получаем общую статистику по рассылкам    
    def list(self, request, *args, **kwargs):
        serializer = MessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        #подсчитываем отправленные сообщения по каждой рассылке, в которых они есть
        sent_messages = Message.objects.filter(status='sent').values('distribution').annotate(total=Count('id'))
        #подсчитываем неотправленные сообщения по каждой рассылке, в которых они есть
        unsent_messages = Message.objects.filter(status='not sent').values('distribution').annotate(total=Count('id'))

        #формируем словари в формате {<id рассылки>: <количество отправленных/неотправленных сообщений по ней>, ...}
        sent_messages = {query['distribution']: query['total'] for query in sent_messages}
        unsent_messages = {query['distribution']: query['total'] for query in unsent_messages}

        #отправляем клиентуобщую статистику по рассылкам с группировкой по статусу сообщений
        return Response({'sent': sent_messages, 'unsent': unsent_messages})