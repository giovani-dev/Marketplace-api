from django.db import models

# Create your models here.
class Client(models.Model):
    full_name = models.CharField(max_length=200, blank=True, null=False)
    cpf = models.CharField(max_length=200, blank=True, null=False)
    email = models.EmailField(max_length=200, blank=True, null=False)
    telephone = models.CharField(max_length=200, blank=True, null=False)
    net_salary = models.FloatField(blank=False, null=True)

    class Meta:
        db_table = 'client'