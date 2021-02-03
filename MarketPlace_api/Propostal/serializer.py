# from rest_framework import serializers
# from Propostal.models import Propostal
# from Client.serializer import SerializeClient
# from Offers.serializer import SerializeOffers
# from datetime import datetime
# from Lib.Offers import OffersComponent
# import requests
# import copy


# class SerializePropostal(serializers.ModelSerializer):
#     client = serializers.DictField(child=serializers.CharField())
#     offer = serializers.DictField(child=serializers.CharField())

#     class Meta:
#         model = Propostal
#         fields = (
#             'client',
#             'offer',
#             # 'date_send',
#             'date_received'
#         )

#     def clean_offer(self, query_offer, request_offer):
#         new_dict = dict()
#         for key in query_offer.__dict__:
#             if key in request_offer.keys():
#                 new_dict.update({ key: query_offer.__dict__[key] })
#         reut

#     def create(self, validated_data):
#         print(validated_data)
#         instance = self.Meta.model.objects.create(date_send=datetime.now())
        
#         offers = OffersComponent().search(client=validated_data['client'])
        
#         request_offer_filtrated = { value: float(validated_data['offer'][value]) for value in validated_data['offer'] if value != 'partner_name' }
#         validated_data['offer'].update(request_offer_filtrated)        
        
#         for offer in offers.get_queryset():
#             copy_offer = copy.deepcopy(offer)
#             # del copy_offer.__dict__['_state']
#             # del copy_offer.__dict__['id']
#             # del copy_offer.__dict__['history_id']
#             # del copy_offer.__dict__['_django_version']
#             new_dict = dict()
#             for key in copy_offer.__dict__:
#                 if key in validated_data['offer'].keys():
#                     new_dict.update({ key: copy_offer.__dict__[key] })

#             print(new_dict)
#             # if new_dict == validated_data['offer']:
#             #     instance.offer = offer


#         return instance