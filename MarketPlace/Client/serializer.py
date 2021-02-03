from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from Client.models import Client

from Util.Validations.cpf import ValidateCpf

import re


class SerializeClient(serializers.ModelSerializer):
    full_name = serializers.CharField(required=True)
    cpf = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    telephone = serializers.CharField(required=True)
    net_salary = serializers.FloatField(required=True)

    class Meta:
        model = Client
        fields = (
            'full_name',
            'cpf',
            'email',
            'telephone',
            'net_salary'
        )
    
    def raise_error(self, msg, validation):
        if not bool(validation):
            raise ValidationError(msg)

    def validate_cpf(self, data):
        validation = ValidateCpf(cpf_text=data, full_validation=True)
        self.raise_error(msg="CPF Invalido", validation=validation)
        return data

    def validate_telephone(self, data):
        validation = True if len(re.findall(r'\d', data)) == 11 else False
        self.raise_error(msg="Telefone Invalido, ele deve conter 11 numeros", validation=validation)
        return data

    def validate_full_name(self, data):
        validation = re.findall(r'\D\s\D', data)
        self.raise_error(msg="Insira um nome completo", validation=validation)
        return data

    def create(self, validated_data):
        client, _ = self.Meta.model.objects.get_or_create(**validated_data)
        return client