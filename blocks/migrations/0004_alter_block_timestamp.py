# Generated by Django 4.2.7 on 2023-11-06 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blocks', '0003_alter_block_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='block',
            name='timestamp',
            field=models.IntegerField(blank=True, default=None, null=True, verbose_name='timestamp'),
        ),
    ]