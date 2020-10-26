
import json
import logging
from .models import Transaction as TransactionModel
from django.forms.models import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View


logger = logging.getLogger(__name__)


class Transaction(View):
    def get(self, request, *args, **kwargs):
        try:
            hash = kwargs.get('hash')
            data = json.dumps( model_to_dict( TransactionModel.objects.get(hash=hash) ) )

            response = render(request, 'transaction/index.html', {
                'serialized_object': data
            }) if not request.GET.get('type', '') == 'json' else HttpResponse(data)

            return response
        except Exception as e:
            logger.error(str(e))
            return HttpResponse('<b>Error</b>')
