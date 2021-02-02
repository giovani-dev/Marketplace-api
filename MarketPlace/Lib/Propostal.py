from rest_framework.exceptions import ValidationError
from Propostal.models import Propostal
from Lib.Offers import OffersComponent
from datetime import datetime, timedelta
import requests, json, copy
from typing import Any


class ValidatePropostal(object):

    # -> self.validate()
    @staticmethod
    def received_data(data) -> dict:
        client = data.get('client', None)
        offer = data.get('offer', None)
        if not client or client == '':
            raise ValidationError({ "client": ["Campo Obrigatorio"] })
        if not offer or offer == '':
            raise ValidationError({ "offer": ["Campo Obrigatorio"] })
        return data

    # -> self.is_valid_offer()
    @staticmethod
    def is_valid_offer(query_offer: object, request_offer: dict) -> bool:
        copy_offer = copy.deepcopy(query_offer)
        del copy_offer.__dict__['_state']
        del copy_offer.__dict__['id']
        del copy_offer.__dict__['history_id']
        del copy_offer.__dict__['_django_version']
        return copy_offer.__dict__ == request_offer

    @staticmethod
    def client_have_a_propostal(delay_time_in_days: int, propostal_id: int, propostal_client: object) -> bool:
        future = datetime.now().date() + timedelta(days=delay_time_in_days)
        try:
            last_propostal = Propostal.objects.all().exclude(id=propostal_id)
            last_propostal.get(date_send__lt=future, client=propostal_client)
            return True
        except Propostal.DoesNotExist:
            return False
        except Propostal.MultipleObjectsReturned:
            return True

class PropostalServiceError(Exception):
    def __init__(self, request_code):
        self.message = f"Invalid request. Error code {request_code}"
        super().__init__()

    def __str__(self):
        return self.message


class DecodeJsonError(Exception):
    def __init__(self, class_name, method_name):
        self.message = f"Can`t decode a json in {class_name}.{method_name}"
        super().__init__()

    def __str__(self):
        return self.message

class PropostalService(object):
    def __init__(self):
        self.response = object()
        self.text = None

    def __iter__(self):
        return iter(self.text)

    def __getitem__(self, key: str):
        return self.text[key]

    def request(self, raise_exception: bool) -> object:
        self.response = requests.post('https://b5c49244-9620-485d-9b32-806899842a22.mock.pstmn.io/proposal', json=local_request_data)
        if raise_exception and self.response.status_code >= 300:
            raise PropostalServiceError(request_code=self.response.status_code)
        return self

    def decode_to_json(self) -> object:
        try:
            self.text = json.loads(self.response.text)
        except Exception:
            raise DecodeJsonError(class_name=self.__class__.__name__, method_name=self.decode_to_json.__name__)
        return self


class ManipulatePropostalModel(object):

    @staticmethod
    def update_propostal(self, instance_to_update: object, **params):
        instance_to_update.udpate(**params)

class PropostalComponent(object):
    def __init__(self, data):
        self.validated_data = ValidatePropostal.received_data(data)# self.validate(data)
        self.propostal_service = PropostalService
        self.validate = ValidatePropostal

    def __iter__(self):
        return iter(self.message)
    
    def __getitem__(self, key):
        return {"message": self.message}[key]

    def send_request_to_service(self, local_request_data: dict, instance_propostal: object):
        now = datetime.now().date() + timedelta(days=30)
        try:
            assert self.validate.client_have_a_propostal(delay_time_in_days=30, propostal_id=instance_propostal.id, propostal_client=instance_propostal.client)
            self.message = {"detail": "Voce ja enviou uma proposta, entretanto ela sera enviada para analise dentro de 30 dias."}
        except AssertionError:
            sended_propostal = self.propostal_service().request(raise_exception=True).decode_to_json()
            ManipulatePropostalModel.update_propostal(instance_to_update=instance_propostal, propostal_id=sended_propostal['propostal_id'], message=sended_propostal['propostal_id'])
            self.message = {
                "proposal_id": self.instance.propostal_id,
                "message": self.instance.message
            }

    def create(self):
        self.instance = Propostal.objects.create(date_send=datetime.now())
        self.offers = OffersComponent().search(client=self.validated_data['client'])

        request_offer_filtrated = { value: float(self.validated_data['offer'][value]) for value in self.validated_data['offer'] if value != 'partner_name' }
        self.validated_data['offer'].update(request_offer_filtrated)
        is_related = False   
        try:
            for offer in self.offers.get_queryset():
                if self.validate.is_valid_offer(query_offer=offer, request_offer=self.validated_data['offer']):# self.is_valid_offer(query_offer=offer, request_offer=self.validated_data['offer']):
                    is_related = True
                    self.instance.offer = offer
                    self.instance.client = self.offers.get_client()
                    self.instance.save()
                    self.send_request_to_service(local_request_data=self.validated_data, instance_propostal=self.instance)
        except Exception as e:
            self.instance.delete()
            raise e
        if not is_related:
            raise ValidationError({ "Offer": ["Informe uma oferta valida."] })
        return self