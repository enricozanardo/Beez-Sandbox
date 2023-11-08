# Generated by Django 4.2.7 on 2023-11-07 22:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('collection', '0002_remove_collections_address_receiver'),
        ('wallets', '0006_wallet_called_exchange'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assets',
            fields=[
                ('id', models.TextField(default=None, primary_key=True, serialize=False, verbose_name='id')),
                ('file', models.TextField(default=None, verbose_name='file')),
                ('name', models.CharField(default=None, verbose_name='name')),
                ('signature', models.CharField(blank=True, default=None, max_length=255, null=True, verbose_name='signature')),
                ('timestamp', models.IntegerField(blank=True, default=None, null=True, verbose_name='timestamp')),
                ('collections', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='collection.collections')),
                ('wallet', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='wallets.wallet')),
            ],
            options={
                'verbose_name': 'Asset',
                'verbose_name_plural': 'Assets',
            },
        ),
    ]