# Generated by Django 4.2.7 on 2023-11-07 10:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blocks', '0005_alter_block_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='block',
            name='transactions',
        ),
    ]
