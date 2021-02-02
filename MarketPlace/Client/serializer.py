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

    def validate_net_salary(self, data):
        errors = dict()
        temp_err = list()
        print(re.findall(r"\d+[.]\d", str(data) ))
        if not bool(re.findall(r"\d+[.]\d", str(data) )):
            temp_err.append("O salario liquido deve ser um numero com ponto flutuante.")
        if len(temp_err) > 0:
            raise ValidationError(temp_err)
        return data

    def validate_cpf(self, data):
        cpf = data
        validation = ValidateCpf(cpf_text=data, full_validation=True)
        if not bool(validation):
            raise ValidationError("CPF Invalido")
        return data


    def create(self, validated_data):
        client, _ = self.Meta.model.objects.get_or_create(**validated_data)
        return client