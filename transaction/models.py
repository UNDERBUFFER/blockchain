
import logging
from .tasks import check_hashes
from hashlib import sha256
from django.db import models


logger = logging.getLogger(__name__)


class Transaction(models.Model):

    sender = models.TextField()
    recipient = models.TextField()
    sum = models.IntegerField()
    hash = models.TextField(unique=True)

    checked = models.BooleanField(default=False)
    processed = models.BooleanField(default=True)

    def get_hash(self, **kwargs):
        sender = kwargs.get( 'sender', self.sender )
        try:
            try:
                last_hash = self.__class__.objects.get( id=self.id-1 ).hash
            except (TypeError, self.__class__.DoesNotExist) as e:
                logger.error(e)
                last_hash = kwargs.get( 'last_hash', self.__class__.objects.last().hash )
        except Exception as e:
            logger.error(e)
            last_hash = ''

        logger.info('getting hash')
        before_hash = ':'.join({
            'sender': sender,
            'recipient': kwargs.get( 'recipient', self.recipient ),
            'sum': str( kwargs.get( 'sum', self.sum ) ),
            'last_hash': last_hash
        }.values())
        return sha256( before_hash.encode() ).hexdigest()

    def set_hash(self, **kwargs):
        logger.info('setting hash')
        self.hash = self.get_hash( **kwargs )
        return self.hash

    def save(self, *args, check=False, **kwargs):
        self.set_hash()
        res = super().save(*args, **kwargs)
        if check:
            check_hashes.delay()
        return res
