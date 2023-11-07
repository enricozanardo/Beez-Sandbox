from django.db import models
from transactions.models import Transaction
from wallets.models import Wallet


class Collections(models.Model):
    id = models.TextField('id', default=None, null=False, blank=False, primary_key=True)
    name = models.CharField('name', default=None, null=False, blank=False)
    signature = models.CharField('signature', max_length=255, default=None, null=True, blank=True)
    address_receiver = models.CharField('address receiver', max_length=255, default=None, null=True, blank=True)
    wallet = models.ForeignKey(Wallet, default=None, null=True, blank=True, on_delete=models.DO_NOTHING)
    transaction = models.ForeignKey(Transaction, default=None, null=True, blank=True, on_delete=models.DO_NOTHING)
    timestamp = models.IntegerField('timestamp', default=None, null=True, blank=True)

    def __str__(self):
        return self.id

    class Meta:
        app_label = 'collection'
        verbose_name = "Collection"
        verbose_name_plural = "Collections"
