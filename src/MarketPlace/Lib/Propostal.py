from rest_framework.exceptions import ValidationError
from Propostal.models import Propostal
from Lib.Offers import OffersComponent
from datetime import datetime, timedelta
import requests, json, copy


class PropostalComponent(object):
    def __init__(self, data):
        self.validated_data = self.validate(data)

    def __iter__(self):
        return iter(self.message)
    
    def __getitem__(self, key):
        return {"message": self.message}[key]

    def validate(self, data):
        client = data.get('client', None)
        offer = data.get('offer', None)
        if not client or client == '':
            raise ValidationError({ "client": ["Campo Obrigatorio"] })
        if not offer or offer == '':
            raise ValidationError({ "offer": ["Campo Obrigatorio"] })
        return data
    
    def is_valid_offer(self, query_offer: object, request_offer: dict) -> dict:
        copy_offer = copy.deepcopy(query_offer)
        del copy_offer.__dict__['_state']
        del copy_offer.__dict__['id']
        del copy_offer.__dict__['history_id']
        del copy_offer.__dict__['_django_version']
        return copy_offer.__dict__ == request_offer

    def send_request_to_service(self, local_request_data: dict, instance_propostal: object):
        now = datetime.now().date() + timedelta(days=30)
        try:
            last_propostal = Propostal.objects.all().exclude(id=instance_propostal.id)
            last_propostal = last_propostal.get(date_send__lt=now, client=instance_propostal.client)
            print("SOMENTE UMA PROPOSTA CADASTRADA")
            self.message = {"detail": "Voce ja enviou uma proposta, entretanto ela sera enviada para analise dentro de 30 dias."}
        except Propostal.DoesNotExist:
            print("NAO EXISTE PROPOSTA")
            req = requests.post('https://b5c49244-9620-485d-9b32-806899842a22.mock.pstmn.io/proposal', json=local_request_data)
            data_decoded =  json.loads(req.text)
            instance_propostal.propostal_id = data_decoded['proposal_id']
            instance_propostal.message = data_decoded['message']
            instance_propostal.save()
            self.message = {
                "proposal_id": self.instance.propostal_id,
                "message": self.instance.message
            }
        except Propostal.MultipleObjectsReturned:
            print("MAIS DE UMA PROPOSTA CADASTRADA")
            self.message = {"detail": "Voce ja enviou uma proposta, entretanto ela sera enviada para analise dentro de 30 dias."}
            

    def create(self):
        self.instance = Propostal.objects.create(date_send=datetime.now())
        self.offers = OffersComponent().search(client=self.validated_data['client'])

        request_offer_filtrated = { value: float(self.validated_data['offer'][value]) for value in self.validated_data['offer'] if value != 'partner_name' }
        self.validated_data['offer'].update(request_offer_filtrated)
        is_related = False   
        try:
            for offer in self.offers.get_queryset():
                if self.is_valid_offer(query_offer=offer, request_offer=self.validated_data['offer']):
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