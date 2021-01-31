import requests, json, threading, logging
from datetime import datetime

from Offers.models import Offers, OffersHistory
from Offers.serializer import SerializeOffers
from Client.serializer import SerializeClient


class OffersComponent(object):

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

    def get(self, client, update_client=True) -> list:
        instance_client = self.client(client_data=client)
        query = Offers.objects.filter(
            history__date_time_expire__gt=datetime.now(),
            history__client__cpf=client['cpf'],
            history__client__full_name=client['full_name'],
            history__client__email=client['email'],
            history__client__telephone=client['telephone'],
            history__client__net_salary=client['net_salary']
        )
        if query.exists():
            serial = SerializeOffers(query, many=True)
            return serial.data
        else:
            offers_request = requests.post('https://b5c49244-9620-485d-9b32-806899842a22.mock.pstmn.io/offers', json=client)
            print(offers_request.text)
            offers_decoded = json.loads(offers_request.text)
            self.save(response_offer=offers_decoded['offers'], client=instance_client)
            return self.get(client=client, update_client=False)