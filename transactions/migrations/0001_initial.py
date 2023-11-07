# Generated by Django 4.2.7 on 2023-11-06 22:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('blocks', '0004_alter_block_timestamp'),
        ('settings', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.TextField(default=None, primary_key=True, serialize=False, verbose_name='id')),
                ('fee', models.IntegerField(blank=True, default=0, null=True, verbose_name='fee')),
                ('data', models.TextField(default=None, verbose_name='data')),
                ('token', models.TextField(default=None, verbose_name='token')),
                ('address_sender', models.CharField(blank=True, default=None, max_length=255, null=True, verbose_name='address sender')),
                ('address_receiver', models.CharField(blank=True, default=None, max_length=255, null=True, verbose_name='address receiver')),
                ('block', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='blocks.block')),
                ('type_transaction', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='settings.typetransfer')),
            ],
            options={
                'verbose_name': 'Transaction',
                'verbose_name_plural': 'Transactions',
            },
        ),
    ]
