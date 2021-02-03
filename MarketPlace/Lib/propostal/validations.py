from rest_framework.exceptions import ValidationError
from Propostal.models import Propostal
from datetime import datetime, timedelta
from typing import Any
import copy


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

    @staticmethod
    def is_propostal_related(is_related) -> None:
        if not is_related:
            raise ValidationError({ "Offer": ["Informe uma oferta valida."] })