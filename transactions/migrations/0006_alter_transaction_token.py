# Generated by Django 4.2.7 on 2023-11-07 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0005_transaction_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='token',
            field=models.TextField(blank=True, default=None, null=True, verbose_name='token'),
        ),
    ]
