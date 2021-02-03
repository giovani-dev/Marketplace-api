from django.db import models
from datetime import datetime, timedelta
from Client.models import Client


class OffersHistory(models.Model):
    date_time_generated = models.DateTimeField(auto_now_add=True)
    date_time_expire = models.DateTimeField(null=False, blank=False)
    is_expired = models.BooleanField(default=False)
    client = models.ForeignKey(Client, related_name='client_offers', on_delete=models.PROTECT, null=True, blank=False)

    class Meta:
        db_table = 'offers_history'

    def save(self, *args, **kwargs):
        expire = datetime.now() + timedelta(minutes=10)
        self.date_time_expire = expire
        super(OffersHistory, self).save(*args, **kwargs)


class Offers(models.Model):
    partner_id = models.IntegerField(blank=True, null=False)
    partner_name = models.CharField(max_length=200, null=False, blank=True)
    value = models.FloatField(blank=False, null=True)
    tax_rate_percent_montly = models.FloatField(blank=False, null=True)
    total_value = models.FloatField(blank=False, null=True)
    installments = models.IntegerField(blank=False, null=True)
    history = models.ForeignKey(OffersHistory,  related_name="fk_offers_history", on_delete=models.CASCADE, null=True, blank=False)

    class Meta:
        db_table = "offers"