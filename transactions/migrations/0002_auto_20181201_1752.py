# Generated by Django 2.1.3 on 2018-12-01 16:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='receivedpayment',
            name='name',
        ),
        migrations.RemoveField(
            model_name='sentpayment',
            name='name',
        ),
    ]
