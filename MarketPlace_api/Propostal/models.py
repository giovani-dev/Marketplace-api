from django.db import models
from Client.models import Client
from Offers.models import Offers


# Create your models here.
class Propostal(models.Model):
    client = models.ForeignKey(Client, related_name='client_propostal', null=True, blank=False, on_delete=models.PROTECT)
    offer = models.ForeignKey(Offers, related_name='offer_propostal', null=True, blank=False, on_delete=models.PROTECT)
    date_send = models.DateField(null=True, blank=True)
    date_received = models.DateField(auto_now_add=True)
    propostal_id = models.IntegerField(null=True, blank=False)
    message = models.TextField(null=False, blank=True)

    class Meta:
        db_table = "propostals"