from Lib.propostal.validations import *
from Lib.propostal.errors import *
from Lib.propostal.service import *

from Offers.models import Offers

from rest_framework.exceptions import ValidationError
from Lib.Offers import OffersComponent
from datetime import datetime, timedelta
import requests, json, copy
from typing import Any

class ProposalDataTreat(object):
    def __init__(self, validated_data):
        self.validated_data = validated_data

    def __iter__(self):
        return iter(self.validated_data)

    def __getitem__(self, key):
        return self.validated_data[key]

    def filter_offer(self) -> dict:
        request_offer_filtrated = { value: float(self.validated_data['offer'][value]) for value in self.validated_data['offer'] if value != 'partner_name' }
        self.validated_data['offer'].update(request_offer_filtrated)
        return self.validated_data


class ManipulatePropostalModel(object):

    @staticmethod
    def update(instance_to_update: object, **params):
        instance_to_update.date_send=datetime.now()
        instance_to_update.propostal_id = params['propostal_id']
        instance_to_update.message = params['message']
        instance_to_update.save()

class PropostalComponent(object):
    def __init__(self, data=None):
        if data:
            self.validated_data = self.set_validated_date(data=data)
            self.is_related = False
        self.propostal_service = PropostalService
        self.validate = ValidatePropostal

    def __iter__(self):
        return iter(self.message)
    
    def __getitem__(self, key: str):
        # criar classe para especificar algum erro de indice
        return {"message": self.message}[key]

    def set_validated_date(self, data: dict) -> dict:
        validated_data = ValidatePropostal.received_data(data)
        return ProposalDataTreat(validated_data=validated_data).filter_offer()

    def send_request_to_service(self, local_request_data: dict, instance_propostal: object):
        try:
            assert self.validate.client_have_a_propostal(delay_time_in_days=30, propostal_id=instance_propostal.id, propostal_client=instance_propostal.client)
            print('nao atualiza')
            self.message = {"detail": "Voce ja enviou uma proposta, entretanto ela sera enviada para analise dentro de 30 dias."}
        except AssertionError:
            sended_propostal = self.propostal_service().request(raise_exception=True, body=local_request_data['client']).decode_to_json()
            print(sended_propostal.text)
            ManipulatePropostalModel.update(instance_to_update=instance_propostal, propostal_id=sended_propostal['proposal_id'], message=sended_propostal['message'])
            self.message = {
                "proposal_id": self.instance.propostal_id,
                "message": self.instance.message
            }

    def update_propostal(self, offer):
        if self.validate.is_valid_offer(query_offer=offer, request_offer=self.validated_data['offer']):# self.is_valid_offer(query_offer=offer, request_offer=self.validated_data['offer']):
            self.is_related = True
            self.instance.offer = offer
            self.instance.client = self.offers.get_client()
            self.instance.save()
            self.send_request_to_service(local_request_data=self.validated_data, instance_propostal=self.instance)

    def create(self):
        self.instance = Propostal.objects.create()
        self.offers = OffersComponent().search(client=self.validated_data['client'])
        
        try:
            for offer in self.offers.get_queryset():
                self.update_propostal(offer=offer)
        except Exception as e:
            self.instance.delete()
            raise e
        self.validate.is_propostal_related(is_related=self.is_related)
        return self