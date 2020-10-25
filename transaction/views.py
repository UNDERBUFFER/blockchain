
import logging
from .models import Transaction as TransactionModel
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View


logger = logging.getLogger(__name__)


class Transaction(View):
    def get(self, request, *args, **kwargs):
        try:
            hash = kwargs.get('hash')
            data = serializers.serialize("json", [TransactionModel.objects.get(hash=hash)])
            return render(request, 'transaction/index.html', {
                'serialized_object': data
            })
        except Exception as e:
            logger.error(str(e))
            return HttpResponse('<b>Error</b>')
