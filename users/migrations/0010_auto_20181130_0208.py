# Generated by Django 2.1.3 on 2018-11-30 01:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20181130_0150'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=200, verbose_name='Country')),
                ('address', models.CharField(max_length=200, verbose_name='Address')),
                ('state', models.CharField(max_length=200, verbose_name='State/Region')),
                ('postal_code', models.CharField(max_length=100, verbose_name='Postal Code')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='postal_code',
            field=models.CharField(blank=True, max_length=100, verbose_name='Postal Code'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user_no',
            field=models.IntegerField(default=5438456789, unique=True, verbose_name='User ID'),
        ),
    ]
