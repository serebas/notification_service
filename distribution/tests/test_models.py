import pytest

from distribution.models import *

class BaseTests:
    def base_create_test(self, obj, model):
        assert obj == model.objects.get(pk=obj.pk)
        attrs = list(obj.__dict__.keys())[2:]
        for attr in attrs:
            assert hasattr(obj, str(attr))

    def base_filter_test(self, obj, model):
        assert model.objects.filter(pk=obj.pk)

    def base_delete_test(self, obj, model):
        obj.delete()
        assert not model.objects.filter(pk=obj.pk).exists()


class TestDisctribution(BaseTests):
    def test_create_disctribution(self, distribution_one):
        self.base_create_test(distribution_one, Distribution)

    def test_filter_disctribution(self, distribution_one):
        self.base_filter_test(distribution_one, Distribution)

    def test_update_disctribution(self, distribution_one):
        message_text = 'Second message'
        filter = 'MNC'
        distribution_one.message_text = message_text
        distribution_one.filter = filter
        distribution_one.save()
        distribution_from_db = Distribution.objects.get(message_text=message_text)
        assert distribution_from_db.filter == filter

    def test_delete_distribution(self, distribution_one):
        self.base_delete_test(distribution_one, Distribution)
        

    
class TestClient(BaseTests):
    def test_create_client(self, client_one):
        self.base_create_test(client_one, Client)

    def test_filter_client(self, client_one):
        self.base_filter_test(client_one, Client)

    def test_update_client(self, client_one):
        phone_number = '79145554312'
        timezone = 'Europe/Moscow'
        client_one.phone_number = phone_number
        client_one.timezone = timezone
        client_one.save()
        client_from_db = Client.objects.get(pk=client_one.pk)
        assert client_from_db.phone_number == phone_number
        assert client_from_db.timezone == timezone

    def test_delete_client(self, client_one):
        self.base_delete_test(client_one, Client)


class TestMessage(BaseTests):
    def test_create_message(self, message_one):
        self.base_create_test(message_one, Message)

    def test_filter_message(self, message_one):
        self.base_filter_test(message_one, Message)

    def test_delete_message(self, message_one):
        self.base_delete_test(message_one, Message)