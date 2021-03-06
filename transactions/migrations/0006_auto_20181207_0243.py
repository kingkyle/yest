# Generated by Django 2.1.3 on 2018-12-07 01:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0005_auto_20181202_0736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receivedpayment',
            name='receiver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='r_receiver', to=settings.AUTH_USER_MODEL, verbose_name='TO'),
        ),
        migrations.AlterField(
            model_name='receivedpayment',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='r_sender', to=settings.AUTH_USER_MODEL, verbose_name='From'),
        ),
        migrations.AlterField(
            model_name='sentpayment',
            name='receiver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='s_receiver', to=settings.AUTH_USER_MODEL, verbose_name='To'),
        ),
        migrations.AlterField(
            model_name='sentpayment',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='s_sender', to=settings.AUTH_USER_MODEL, verbose_name='From'),
        ),
    ]
