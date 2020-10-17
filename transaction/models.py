
import asyncio
from hashlib import sha256
from django.db import models


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
            print(e)
            last_hash = ''

        before_hash = ':'.join({
            'sender': sender,
            'recipient': kwargs.get( 'recipient', self.recipient ),
            'sum': str( kwargs.get( 'sum', self.sum ) ),
            'last_hash': last_hash
        }.values())
        return sha256( before_hash.encode() ).hexdigest()

    def set_hash(self, **kwargs):
        self.hash = self.get_hash(**kwargs)
        return self.hash

    # @classmethod
    # def check_hashes(*cls, *objects):
    #     for index, object in enumerate(objects):
    #         if index != 0:
    #             hash1 = object.get_hash( last_hash=object.hash )
    #             hash2 = object.get_hash( last_hash=objects[index-1].hash )
    #             if hash1 != hash2:
    #                 return False
    #     return True

    # @classmethod
    # async def check_transactions(*cls):

