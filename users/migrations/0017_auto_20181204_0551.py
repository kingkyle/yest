# Generated by Django 2.1.3 on 2018-12-04 04:51

from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_auto_20181202_0904'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='country',
            field=django_countries.fields.CountryField(max_length=2, verbose_name='Country'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='country',
            field=django_countries.fields.CountryField(max_length=2, verbose_name='Country'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone',
            field=models.IntegerField(verbose_name='Phone Number'),
        ),
    ]
