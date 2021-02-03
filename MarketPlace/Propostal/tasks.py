from __future__ import absolute_import, unicode_literals
from celery import shared_task
from datetime import datetime, timedelta
from Propostal.models import Propostal
from Client.serializer import SerializeClient
from Lib.Propostal import ManipulatePropostalModel
from Lib.propostal.service import PropostalService

# @shared_task()
def task_verify_propostal():
    now = datetime.now().date()
    future = datetime.now().date() + timedelta(days=30)
    query_propostal = Propostal.objects.filter(date_received__gte=future, date_send=None)
    print(query_propostal)
    for propostal in query_propostal:
        client = SerializeClient(propostal.client, many=False).data
        response = PropostalService().request(raise_exception=True, body=client).decode_to_json()
        ManipulatePropostalModel.update(instance_to_update=propostal, propostal_id=response['proposal_id'], message=response['message'])