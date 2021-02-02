from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.shortcuts import render
# from Propostal.serializer import SerializePropostal
from Lib.Propostal import PropostalComponent

# Create your views here.
class PropostalSend(generics.CreateAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        propostal = PropostalComponent(data=self.request.data).create()
        message = propostal['message']
        return Response(message)

