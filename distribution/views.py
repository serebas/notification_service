from rest_framework.views import *
from rest_framework import mixins, viewsets
from datetime import datetime
from django.db.models import Q
from django.db.models import Count
from django.http import Http404
from .serializers import *
from .models import Message, Distribution
from .tasks import send_message


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

    def create(self, request, *args, **kwargs):
        serializer = DisctributionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        distribution = Distribution.objects.create(**serializer.data)

        timestamp_start = datetime.strptime(serializer.data['timestamp_start'][:-6], "%Y-%m-%dT%H:%M:%S")
        timestamp_end = datetime.strptime(serializer.data['timestamp_end'][:-6], "%Y-%m-%dT%H:%M:%S")
        filter = serializer.data['filter']
        clients = Client.objects.filter(Q(MNC=filter) | Q(TAG=filter))     #список клиентов, подходящих по значению фильтра

        for client in clients:                                              #назначение времени отправки сообщений
            message = Message.objects.create(distribution=distribution, client=client)
            if timestamp_start < datetime.now() < timestamp_end:              #если текущее время больше времени начала, но меньше времени конца рассылки
                send_message.apply_async((message.id,), countdown=1)          #рассылаем сообщения сразу
            elif timestamp_start > datetime.now():                          #если время начала рассылки больше текущего
                send_message.apply_async((message.id,), eta=timestamp_start)  #рассылаем сообщения во время начала рассылки

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        try:
            messages = Message.objects.filter(distribution_id=pk, status='sent')
            serializer = MessageSerializer(messages, many=True)
            return Response(serializer.data)
        except:
            return Response({'detail': 'Указан неверный id'}, status=status.HTTP_204_NO_CONTENT)
    

class StatisticViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
        
    def list(self, request, *args, **kwargs):
        sent_messages = Message.objects.filter(status='sent').values('distribution').annotate(total=Count('id'))
        unsent_messages = Message.objects.filter(status='not sent').values('distribution').annotate(total=Count('id'))

        serializer = MessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        sent_messages = {query['distribution']: query['total'] for query in sent_messages}
        unsent_messages = {query['distribution']: query['total'] for query in unsent_messages}

        return Response({'sent': sent_messages, 'unsent': unsent_messages})