# Generated by Django 3.0 on 2019-12-19 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('s_store_api', '0005_wallet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='value',
            field=models.IntegerField(default=0),
        ),
    ]
