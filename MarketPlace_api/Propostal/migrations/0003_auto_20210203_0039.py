# Generated by Django 3.1.5 on 2021-02-03 03:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Propostal', '0002_auto_20210202_1856'),
    ]

    operations = [
        migrations.AlterField(
            model_name='propostal',
            name='date_send',
            field=models.DateField(blank=True, null=True),
        ),
    ]