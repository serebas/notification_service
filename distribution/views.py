from rest_framework import viewsets
from rest_framework.views import *
from rest_framework import mixins, generics, viewsets
from .serializers import *
from datetime import datetime
from django.db.models import Q
from .models import Message, Distribution

class ClientViewSet(mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    

class DistributionViewSet(mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    
    queryset = Distribution.objects.all()
    serializer_class = DisctributionSerializer

    def create(self, request, *args, **kwargs):
        serializer = DisctributionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        distribution = Distribution.objects.create(**serializer.data)
        print(distribution)

        timestamp_start = serializer.data['timestamp_start']
        if datetime.now() > timestamp_start:
            filter = serializer.data['filter']
            clients = Client.objects.filter(Q(MNC=filter) | Q(TAG=filter))
            for client in clients:
                message = Message.objects.create(distribution=distribution, client=client)
                #сразу отправить сообщение всем пользователям
            
        else:
            pass
            #запланировать отправку сообщений в назначенное время (timestamp_start)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
