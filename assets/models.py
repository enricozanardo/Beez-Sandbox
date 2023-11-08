from django.db import models
from collection.models import Collections
from wallets.models import Wallet


class Assets(models.Model):
    id = models.TextField('id', default=None, null=False, blank=False, primary_key=True)
    file = models.TextField('file', default=None, null=False, blank=False)
    name = models.CharField('name', default=None, null=False, blank=False)
    amount = models.IntegerField('amount', default=0, null=False, blank=False)
    signature = models.CharField('signature', max_length=255, default=None, null=True, blank=True)
    wallet = models.ForeignKey(Wallet, default=None, null=True, blank=True, on_delete=models.DO_NOTHING)
    collections = models.ForeignKey(Collections, default=None, null=True, blank=True, on_delete=models.DO_NOTHING)
    timestamp = models.IntegerField('timestamp', default=None, null=True, blank=True)

    @property
    def address(self):
        return self.wallet.address

    def __str__(self):
        return self.id

    class Meta:
        app_label = 'assets'
        verbose_name = "Asset"
        verbose_name_plural = "Assets"
