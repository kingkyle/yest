# Generated by Django 2.1.3 on 2018-12-01 16:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import transactions.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ReceivedPayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('amount', models.IntegerField()),
                ('type', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=100)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('trans_id', models.CharField(default=transactions.models.random_string, editable=False, max_length=225, unique=True)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiver_from', to=settings.AUTH_USER_MODEL, verbose_name='To')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender_to', to=settings.AUTH_USER_MODEL, verbose_name='From')),
            ],
        ),
        migrations.CreateModel(
            name='SentPayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('amount', models.IntegerField()),
                ('type', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=100)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('trans_id', models.CharField(default=transactions.models.random_string, editable=False, max_length=225, unique=True)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiver_to', to=settings.AUTH_USER_MODEL, verbose_name='To')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender_from', to=settings.AUTH_USER_MODEL, verbose_name='From')),
            ],
        ),
    ]
