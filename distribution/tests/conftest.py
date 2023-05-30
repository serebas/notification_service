import pytest
import datetime

from distribution.models import *

@pytest.fixture
def distribution_one(db):
    return Distribution.objects.create(
        message_text='Your first distribution',
        filter='TAG',
        timestamp_start=datetime.datetime.now(),
        timestamp_end=datetime.datetime.now() + datetime.timedelta(hours=1)
    )

@pytest.fixture
def client_one(db):
    return Client.objects.create(
        phone_number='79175182687',
        MNC='7',
        TAG='andrew5',
        timezone='Africa/Abidjan'
    )

@pytest.fixture
def message_one(db, distribution_one, client_one):
    return Message.objects.create(
        timestamp_create = datetime.datetime.now(),
        status='sent',
        distribution=distribution_one,
        client = client_one
    )


