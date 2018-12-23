import string
import random
from django.db import models
from users.models import MyUser


def random_string(string_length=20):
    """Generate a random string with the combination of lowercase and
     uppercase letters """
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(string_length))


class PaymentFee(models.Model):
    fee = models.DecimalField(
        max_digits=19, decimal_places=2, verbose_name='Transaction Fee',
        default=0.00)

    def __str__(self):
        return f'{self.fee} Info'


class SentPayment(models.Model):
    receiver = models.ForeignKey(
        MyUser, on_delete=models.CASCADE, verbose_name='To',
        related_name='s_receiver')
    amount = models.DecimalField(max_digits=19, decimal_places=2)
    trans_type = models.CharField(
        max_length=100, default='Payment To', editable=False)
    status = models.CharField(
        max_length=100, default='Completed', editable=False)
    date = models.DateTimeField(
        auto_now_add=True, editable=False)
    trans_id = models.CharField(
        max_length=225, default=random_string, unique=True, editable=False)
    info = models.CharField(
        max_length=1000, null=True, default='No Payment Info',
        verbose_name='Payment Details')
    fee = models.DecimalField(
        max_digits=19, decimal_places=2, verbose_name='Transaction Fee',
        default=0.00)
    sender = models.ForeignKey(
        MyUser, on_delete=models.CASCADE, verbose_name='From',
        related_name='s_sender')
    sender_balance = models.DecimalField(verbose_name='Sender Balance',
                                         max_digits=19, decimal_places=2,
                                         default=0.00)
    receiver_balance = models.DecimalField(verbose_name='Receiver Balance',
                                           max_digits=19, decimal_places=2,
                                           default=0.00)

    def __str__(self):
        return f'{self.sender.first_name} {self.sender.last_name} PaymentSent'


class ReceivedPayment(models.Model):
    receiver = models.ForeignKey(
        MyUser, on_delete=models.CASCADE, verbose_name='TO',
        related_name='r_receiver')
    amount = models.DecimalField(max_digits=19, decimal_places=2)
    trans_type = models.CharField(
        max_length=100, default='Payment From', editable=False)
    status = models.CharField(
        max_length=100, default='Completed', editable=False)
    date = models.DateTimeField(auto_now_add=True, editable=False)
    trans_id = models.CharField(
        max_length=225, default=random_string, unique=True, editable=False)
    info = models.CharField(
        max_length=1000, null=True, default='No Payment Info',
        verbose_name='Payment Details')
    fee = models.DecimalField(
        max_digits=19, decimal_places=2, verbose_name='Transaction Fee',
        default=0.00)
    sender = models.ForeignKey(
        MyUser, on_delete=models.CASCADE, verbose_name='From',
        related_name='r_sender')
    sender_balance = models.DecimalField(verbose_name='Sender Balance',
                                         max_digits=19, decimal_places=2,
                                         default=0.00)
    receiver_balance = models.DecimalField(verbose_name='Receiver Balance',
                                           max_digits=19, decimal_places=2,
                                           default=0.00)

    def __str__(self):
        return f'{self.receiver.first_name} {self.receiver.last_name} PaymentReceived'
