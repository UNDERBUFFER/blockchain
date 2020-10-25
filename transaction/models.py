
import asyncio
import logging
from asgiref.sync import sync_to_async
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
        self.hash = self.get_hash(**kwargs)
        return self.hash

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        return self.check_hashes( *self.__class__.objects.all().order_by('id').reverse() )


    @classmethod
    async def check_hashes(cls, *objects):

        for index, object in enumerate(objects):

            logger.info('{} processing'.format(object))
            object.processed = True
            object.checked = False
            object.save()
            await asyncio.sleep(5)

            if (index + 1) < len(objects):
                hash1 = object.get_hash( last_hash=object.hash )
                hash2 = object.get_hash( last_hash=objects[index+1].hash )
                if hash1 != hash2:
                    object.processed = False
                    object.checked = False
                else:
                    object.processed = False
                    object.checked = True
            else:
                object.processed = False
                object.checked = True
            object.save()
            await asyncio.sleep(5)

