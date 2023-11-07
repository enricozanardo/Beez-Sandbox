# Generated by Django 4.2.7 on 2023-11-07 15:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wallets', '0006_wallet_called_exchange'),
        ('transactions', '0006_alter_transaction_token'),
    ]

    operations = [
        migrations.CreateModel(
            name='Collections',
            fields=[
                ('id', models.TextField(default=None, primary_key=True, serialize=False, verbose_name='id')),
                ('name', models.CharField(default=None, verbose_name='name')),
                ('signature', models.CharField(blank=True, default=None, max_length=255, null=True, verbose_name='signature')),
                ('address_receiver', models.CharField(blank=True, default=None, max_length=255, null=True, verbose_name='address receiver')),
                ('timestamp', models.IntegerField(blank=True, default=None, null=True, verbose_name='timestamp')),
                ('transaction', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='transactions.transaction')),
                ('wallet', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='wallets.wallet')),
            ],
            options={
                'verbose_name': 'Collection',
                'verbose_name_plural': 'Collections',
            },
        ),
    ]