# Generated by Django 3.0 on 2019-12-23 03:35

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('s_store_api', '0008_auto_20191220_1123'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='store',
            options={'permissions': (('management_store', 'Can management store'),)},
        ),
        migrations.AlterUniqueTogether(
            name='store',
            unique_together={('user', 'name')},
        ),
    ]
