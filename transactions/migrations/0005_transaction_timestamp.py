# Generated by Django 4.2.7 on 2023-11-07 00:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0004_transaction_type_transaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='timestamp',
            field=models.IntegerField(blank=True, default=None, null=True, verbose_name='timestamp'),
        ),
    ]
