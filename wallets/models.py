from django.db import models
from django.contrib.auth.models import User


class Wallet(models.Model):
    mnemonic = models.TextField('mnemonic', default=None, null=True, blank=True)
    address = models.CharField('address', max_length=255, default=None, null=True, blank=True)
    private_key = models.CharField('private key', max_length=255, default=None, null=True, blank=True)
    public_key = models.CharField('public key', max_length=255, default=None, null=True, blank=True)
    balance = models.IntegerField('balance', default=0, null=True, blank=True)
    user = models.ForeignKey(User, default=None, null=True, blank=True, on_delete=models.DO_NOTHING)

    class Meta:
        app_label = 'wallets'
        verbose_name = "Wallet"
        verbose_name_plural = "Wallets"