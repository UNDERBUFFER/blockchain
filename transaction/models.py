
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

    def get_hash(self, is_existed_object=False, **kwargs):
        sender = kwargs.get( 'sender', self.sender )
        try:
            if not is_existed_object:
                last_hash = kwargs.get( 'last_hash', self.__class__.objects.last().hash )
            else:
                last_hash = self.__class__.objects.get( id=self.id-1 ).hash
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

    def set_hash(self, is_existed_object=False, **kwargs):
        logger.info('setting hash')
        self.hash = self.get_hash( is_existed_object=is_existed_object, **kwargs )
        return self.hash

    def save(self, *args, check=False, **kwargs):
        res = super().save(*args, **kwargs)
        if check:
            check_hashes.delay()
        return res
