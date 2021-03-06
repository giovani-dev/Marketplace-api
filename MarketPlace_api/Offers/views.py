from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from django.shortcuts import render

from Offers.serializer import SerializeOffers
from Lib.Offers import OffersComponent


# Create your views here.
class ListOffers(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = SerializeOffers

    def post(self, request, *args, **kwargs):
        offers = OffersComponent().search(client=self.request.data)
        return Response({ "Offers": offers.get_serialized() })