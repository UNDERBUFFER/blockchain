
from django.forms import ModelForm
from transaction.models import Transaction


class Transfer(ModelForm):

    class Meta:
        model = Transaction
        fields = ['sender', 'recipient', 'sum']
