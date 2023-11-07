from django.db import models
from settings.models import TypeTransfer
from blocks.models import Block
from django.contrib.auth.models import User


# Create your models here.


# Login tramite email, password, --> se non esiste crea il wallet (account) da fare solo get proprio account

# POST di ogni transazione crea un blocco unico (login)
# type, fee, data = varchar, token = integer

# type solo:
# | "EXCHANGE"
# | "TRANSFER"


# upload file
# assets sono i file caricati con uuid --> transazione
# put per associare una collection


# collection (come una folder)

class Transaction(models.Model):
    id = models.TextField('id', default=None, null=False, blank=False, primary_key=True)
    type_transaction = models.ForeignKey(TypeTransfer, default=None, null=True, blank=True, on_delete=models.DO_NOTHING)
    fee = models.IntegerField('fee', default=0, null=True, blank=True)
    data = models.TextField('data', default=None, null=False, blank=False)
    token = models.TextField('token', default=None, null=False, blank=False)
    address_sender = models.CharField('address sender', max_length=255, default=None, null=True, blank=True)
    signature = models.CharField('signature', max_length=255, default=None, null=True, blank=True)
    address_receiver = models.CharField('address receiver', max_length=255, default=None, null=True, blank=True)
    block = models.ForeignKey(Block, default=None, null=True, blank=True, on_delete=models.DO_NOTHING)
    timestamp = models.IntegerField('timestamp', default=None, null=True, blank=True)

    def __str__(self):
        return self.id

    class Meta:
        app_label = 'transactions'
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"


