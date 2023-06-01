from rest_framework import serializers
from .models import *

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class DisctributionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Distribution
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'