from django.db import models


class TypeTransfer(models.Model):
    key = models.CharField('key', max_length=255, default=None, null=False, blank=False, primary_key=True)
    description = models.TextField('description', default=None, null=True, blank=True)
    fee = models.IntegerField('fee', default=0, null=True, blank=True)

    def __str__(self):
        return self.key

    class Meta:
        app_label = 'settings'
        verbose_name = "Type Transfer"
        verbose_name_plural = "Types Transfer"
