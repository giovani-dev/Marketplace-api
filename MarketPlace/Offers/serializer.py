from rest_framework import serializers
from Offers.models import Offers


class SerializeOffers(serializers.ModelSerializer):

    class Meta:
        model = Offers
        fields = (
            'partner_id',
            'partner_name',
            'value',
            'tax_rate_percent_montly',
            'total_value',
            'installments'
        )