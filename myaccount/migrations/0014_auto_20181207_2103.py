# Generated by Django 2.1.3 on 2018-12-07 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myaccount', '0013_notifiercount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notifiercount',
            name='count',
            field=models.IntegerField(),
        ),
    ]