import json

from django.db import models


class Block(models.Model):
    id = models.CharField('id', max_length=255, default=None, null=False, blank=False, primary_key=True)
    block_count = models.IntegerField('block count', default=0, null=True, blank=True)
    forger = models.CharField('forger', max_length=255, default=None, null=True, blank=True)
    last_hash = models.CharField('last hash', max_length=255, default=None, null=True, blank=True)
    signature = models.CharField('signature', max_length=255, default=None, null=True, blank=True)
    timestamp = models.IntegerField('timestamp', default=None, null=True, blank=True)

    @property
    def transactions(self):
        transactions_list = self.transaction_set.all()
        content = []
        for item_trans in transactions_list:
            temp = {
                "type_transaction": item_trans.type_transaction.key,
                "fee": item_trans.fee,
                "data": item_trans.data,
                "token": item_trans.token,
                "address_sender": item_trans.address_sender,
                "address_receiver": item_trans.address_receiver,
                "signature": item_trans.signature,
                "timestamp": item_trans.timestamp,
            }
            content.append(temp)
        return content

    def __str__(self):
        return self.id

    class Meta:
        app_label = 'blocks'
        verbose_name = "Block"
        verbose_name_plural = "Blocks"
