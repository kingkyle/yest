# Generated by Django 2.1.3 on 2018-12-07 17:44

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('myaccount', '0011_notifier'),
    ]

    operations = [
        migrations.AddField(
            model_name='notifier',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
