
import logging
from blockchain.celery import app


logger = logging.getLogger(__name__)


@app.task
def check_hashes():

    from .models import Transaction
    objects = Transaction.objects.all().order_by('id').reverse()

    for index, object in enumerate(objects):

        logger.info('{} processing'.format(object))
        object.processed = True
        object.checked = False
        object.save()

        if (index + 1) < len(objects):
            hash1 = object.hash
            hash2 = object.get_hash( last_hash=objects[index+1].hash )
            if hash1 != hash2:
                logger.warning('hash1<{}> != hash2<{}>'.format( hash1, hash2 ))
                object.processed = False
                object.checked = False
            else:
                object.processed = False
                object.checked = True
        else:
            object.processed = False
            object.checked = True
        object.save()

    return True
