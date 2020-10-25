
import logging
from .forms import Transfer as TransferForm
from transaction.models import Transaction as TransactionModel
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View


logger = logging.getLogger(__name__)


class Transfer(View):

    def get(self, request, *args, **kwargs):
        form = TransferForm()
        return render(request, 'transfer/index.html', {
            'form': form
        })

    def post(self, request, *args, **kwargs):
        data = {
            'sender': request.POST.get('sender', None),
            'recipient': request.POST.get('recipient', None),
            'sum': request.POST.get('sum', None)
        }

        try:
            transaction = TransactionModel(**data)
            hash_id = transaction.set_hash()
            transaction.save(check=True)
            return redirect('/transaction/{}'.format(hash_id))
        except Exception as e:
            logger.error(str(e))
            return HttpResponse('<b>Error</b>')