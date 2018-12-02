from django.db import models
from users.models import MyUser, Address
from django.urls import reverse


class Notification(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    send_payment = models.BooleanField(verbose_name='Send Payment', default=True)
    receive_payment = models.BooleanField(verbose_name='Receive Payment')
    surveys = models.BooleanField(verbose_name='Surveys')
    news = models.BooleanField(verbose_name='New and Promotions')
    info_update = models.BooleanField(verbose_name='information Update', default=True)
    address_update = models.BooleanField(verbose_name='Address Update')
    bank_update = models.BooleanField(verbose_name='Bank Update')
    card_update = models.BooleanField(verbose_name='Card Update')

    def __str__(self):
        return f'{self.user.email} Notifications'


class Balance(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    available_balance = models.DecimalField(verbose_name='Available Balance', max_digits=19, decimal_places=2, default=0.00)
    pending_balance = models.DecimalField(verbose_name='Pending Balance', default=0.00, max_digits=19, decimal_places=2,
                                          blank=True)

    def __str__(self):
        return f'{self.user.email} Balance'

    def get_balance(self):
        return self.available_balance


class Card(models.Model):
    MASTERCARD = 'MC'
    VISA = 'VS'
    CARD_TYPE_CHOICES = (
        (MASTERCARD, 'MasterCard'),
        (VISA, 'Visa')
    )
    ccards = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    card_no = models.IntegerField(verbose_name='Credit Card Number')
    exp_date = models.CharField(verbose_name='Expiration Date', max_length=10)
    card_type = models.CharField(verbose_name='Card Type', max_length=2, choices=CARD_TYPE_CHOICES, default=MASTERCARD)
    security_code = models.IntegerField(verbose_name='Security Code')
    billing_address = models.ForeignKey(Address, verbose_name='Billing Address', on_delete=models.PROTECT)

    def __str__(self):
        return f'{user.email} Card'

    def get_absolute_url(self):
        return reverse('myaccount-payment')

