# Generated by Django 2.1.3 on 2018-12-02 06:36

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0004_auto_20181201_2320'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detail', models.TextField(blank=True, max_length=1000, null=True, verbose_name='Payment Information')),
                ('fee', models.DecimalField(decimal_places=2, default=0.0, max_digits=19, verbose_name='Transaction Fee')),
            ],
        ),
        migrations.AlterField(
            model_name='receivedpayment',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=19),
        ),
        migrations.AlterField(
            model_name='receivedpayment',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AlterField(
            model_name='receivedpayment',
            name='status',
            field=models.CharField(default='Completed', editable=False, max_length=100),
        ),
        migrations.AlterField(
            model_name='receivedpayment',
            name='type',
            field=models.CharField(default='Payment From', editable=False, max_length=100),
        ),
        migrations.AlterField(
            model_name='sentpayment',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=19),
        ),
        migrations.AlterField(
            model_name='sentpayment',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AlterField(
            model_name='sentpayment',
            name='status',
            field=models.CharField(default='Completed', editable=False, max_length=100),
        ),
        migrations.AlterField(
            model_name='sentpayment',
            name='type',
            field=models.CharField(default='Payment To', editable=False, max_length=100),
        ),
        migrations.AddField(
            model_name='paymentinfo',
            name='payment_info',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transactions.SentPayment'),
        ),
    ]
