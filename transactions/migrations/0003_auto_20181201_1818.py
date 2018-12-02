# Generated by Django 2.1.3 on 2018-12-01 17:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0002_auto_20181201_1752'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receivedpayment',
            name='receiver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_receiver', to=settings.AUTH_USER_MODEL, verbose_name='To'),
        ),
        migrations.AlterField(
            model_name='receivedpayment',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_sender', to=settings.AUTH_USER_MODEL, verbose_name='From'),
        ),
    ]