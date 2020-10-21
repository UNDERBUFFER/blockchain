
from .forms import Transfer as TransferForm
from django.shortcuts import render
from django.views import View


class Transfer(View):
    def get(self, request, *args, **kwargs):
        form = TransferForm()
        return render(request, 'transfer/index.html', {
            'form': form
        })
