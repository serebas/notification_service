import pytest

from distribution.models import *


class TestDisctribution:
    def test_create_disctribution(self, distribution_one):
        assert distribution_one == Distribution.objects.get(pk=distribution_one.pk)
        assert hasattr(distribution_one, 'message_text')
        assert hasattr(distribution_one, 'filter')
        assert hasattr(distribution_one, 'timestamp_start')
        assert hasattr(distribution_one, 'timestamp_end')

    def test_filter_disctribution(self, distribution_one):
        assert Distribution.objects.filter(pk=distribution_one.pk)

    def test_update_disctribution(self, distribution_one):
        message_text = 'Second message'
        filter = 'MNC'
        distribution_one.message_text = message_text
        distribution_one.filter = filter
        distribution_one.save()
        distribution_from_db = Distribution.objects.get(message_text=message_text)
        assert distribution_from_db.filter == filter

    
class TestClient:
    def test_create_client(self, client_one):
        assert client_one == Client.objects.get(pk=client_one.pk)
        assert hasattr(client_one, 'phone_number')
        assert hasattr(client_one, 'MNC')
        assert hasattr(client_one, 'TAG')
        assert hasattr(client_one, 'timezone')

    def test_filter_client(self, client_one):
        assert Client.objects.filter(pk=client_one.pk)

    def test_update_client(self, client_one):
        phone_number = '79145554312'
        timezone = 'Europe/Moscow'
        client_one.phone_number = phone_number
        client_one.timezone = timezone
        client_one.save()
        client_from_db = Client.objects.get(pk=client_one.pk)
        assert client_from_db.phone_number == phone_number
        assert client_from_db.timezone == timezone
