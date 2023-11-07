from django.db import models


class Block(models.Model):
    id = models.CharField('id', max_length=255, default=None, null=False, blank=False, primary_key=True)
    block_count = models.IntegerField('block count', default=0, null=True, blank=True)
    forger = models.CharField('forger', max_length=255, default=None, null=True, blank=True)
    last_hash = models.CharField('last hash', max_length=255, default=None, null=True, blank=True)
    signature = models.CharField('signature', max_length=255, default=None, null=True, blank=True)
    timestamp = models.IntegerField('timestamp', default=None, null=True, blank=True)
    transactions = models.IntegerField('transactions', default=None, null=True, blank=True)

    def __str__(self):
        return self.id

    class Meta:
        app_label = 'blocks'
        verbose_name = "Block"
        verbose_name_plural = "Blocks"
