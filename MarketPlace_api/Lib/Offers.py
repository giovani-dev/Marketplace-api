import requests, json, threading, logging
from datetime import datetime

from Offers.models import Offers, OffersHistory
from Offers.serializer import SerializeOffers
from Client.serializer import SerializeClient


class OffersComponent(object):
    def __init__(self):
        self.query = object()

    def client(self, client_data: dict) -> object:
        serial = SerializeClient(data=client_data)
        serial.is_valid(raise_exception=True)
        return serial.save()

    def save(self, response_offer: dict, client: object) -> None:
        instance_history = OffersHistory.objects.create(client=client)
        for offers in response_offer:
            serial = SerializeOffers(data=offers)
            try:
                serial.is_valid(raise_exception=True)
                serial.save(history=instance_history)
            except Exception as e:
                logging.error(f'In ListOffers view: {e}'.encode('utf-8'))

    def get_queryset(self):
        return self.query

    def get_serialized(self):
        return self.serialized

    def get_client(self):
        return self.instance_client

    def search(self, client, update_client=True) -> list:
        self.instance_client = self.client(client_data=client)
        self.query = Offers.objects.filter(
            history__date_time_expire__gt=datetime.now(),
            history__client__cpf=client['cpf'],
            history__client__full_name=client['full_name'],
            history__client__email=client['email'],
            history__client__telephone=client['telephone'],
            history__client__net_salary=client['net_salary']
        )
        if self.query.exists():
            serial = SerializeOffers(self.query, many=True)
            self.serialized = serial.data
            return self
        else:
            offers_request = requests.post('https://b5c49244-9620-485d-9b32-806899842a22.mock.pstmn.io/offers', json=client)
            offers_decoded = json.loads(offers_request.text)
            self.save(response_offer=offers_decoded['offers'], client=self.instance_client)
            return self.search(client=client, update_client=False)