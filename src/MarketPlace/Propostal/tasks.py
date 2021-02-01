from celery import shared_task
from datetime import datetime, timedelta
from Propostal.models import Propostal


@shared_task
def verify_propostal():
    now = datetime.now().date()
    future = datetime.now().date() + timedelta(days=30)
    query_propostal = Propostal.objects.filter(date_send__lt=future, date_received=None)
    for propostal in query_propostal:
        ...