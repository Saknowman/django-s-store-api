# Generated by Django 3.0 on 2019-12-24 01:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('s_store_api', '0010_cashregister'),
    ]

    operations = [
        migrations.CreateModel(
            name='Receipt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=20)),
                ('item_price', models.CharField(max_length=30)),
                ('item_num', models.IntegerField(default=1)),
                ('store_name', models.CharField(max_length=20)),
                ('sold_date_time', models.DateTimeField(auto_now_add=True)),
                ('item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='receipts', to='s_store_api.Item')),
                ('store', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='receipts', to='s_store_api.Store')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='receipts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
