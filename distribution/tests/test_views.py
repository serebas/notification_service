from rest_framework.test import APIClient
import datetime
APIclient = APIClient()


class TestClient:

    endpoint = '/api/client/'
    payload = dict(phone_number='9115556677', MNC='7', TAG='tag', timezone='Europe/Moscow')

    def post_or_update_assert(self, data, response, code):
        assert response.status_code == code
        assert data['phone_number'] == self.payload['phone_number']
        assert data['timezone'] == self.payload['timezone']

    def test_post_client(self, db):
        response = APIclient.post(self.endpoint, self.payload)
        data = response.data
        self.post_or_update_assert(data, response, code=201)

    def test_put_client(self, db, client_one):
        response = APIclient.put(self.endpoint + f'{client_one.id}/', self.payload)
        data = response.data
        self.post_or_update_assert(data, response, code=200)

    def test_delete_client(self, db, client_one):
        response = APIclient.delete(self.endpoint + f'{client_one.id}/')
        assert response.status_code == 204

class TestDistribution:

    endpoint = '/api/distribution/'
    payload = dict(
            message_text='hello',
            filter='customer',
            timestamp_start=datetime.datetime(2023, 6, 20, 12, 15, 25),
            timestamp_end=datetime.datetime(2023, 6, 21, 12, 15, 25)
        )

    def test_put_distribution(self, db, distribution_one):
        response = APIclient.put(self.endpoint + f'{distribution_one.id}/', self.payload)
        data = response.data

        assert response.status_code == 200
        assert distribution_one.message_text != data['message_text']
        assert distribution_one.filter != data['filter']

    def test_delete_distribution(self, db, distribution_one):
        response = APIclient.delete(self.endpoint + f'{distribution_one.id}/')
        assert response.status_code == 204

    def test_get_statistic(self, db, distribution_one):
        response = APIclient.get(self.endpoint + f'{distribution_one.id}/')
        assert response.status_code == 200


class TestStatistic:
     
     endpoint = '/api/statistic/'

     def test_get_statistic(self, db):
         response = APIclient.get(self.endpoint)
         data = response.data

         assert response.status_code == 200
         assert 'sent' in data and 'unsent' in data