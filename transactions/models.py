import string
import random
from django.db import models
from users.models import MyUser
from django.utils import timezone


def random_string(string_length=20):
    """Generate a random string with the combination of lowercase and uppercase letters """
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(string_length))


class SentPayment(models.Model):
    receiver = models.ForeignKey(MyUser, on_delete=models.CASCADE, verbose_name='To', related_name='receiver_to')
    amount = models.DecimalField(max_digits=19, decimal_places=2)
    type = models.CharField(max_length=100, default='Payment To', editable=False)
    status = models.CharField(max_length=100, default='Completed', editable=False)
    date = models.DateTimeField(default=timezone.now, editable=False)
    trans_id = models.CharField(max_length=225, default=random_string, unique=True, editable=False)
    sender = models.ForeignKey(MyUser, on_delete=models.CASCADE, verbose_name='From', related_name='sender_from')

    def __str__(self):
        return f'{self.sender.first_name} {self.sender.last_name} Payment'


class ReceivedPayment(models.Model):
    receiver = models.ForeignKey(MyUser, on_delete=models.CASCADE, verbose_name='From', related_name='from_receiver')
    amount = models.DecimalField(max_digits=19, decimal_places=2)
    type = models.CharField(max_length=100, default='Payment From', editable=False)
    status = models.CharField(max_length=100, default='Completed', editable=False)
    date = models.DateTimeField(default=timezone.now, editable=False)
    trans_id = models.CharField(max_length=225, default=random_string, unique=True, editable=False)
    sender = models.ForeignKey(MyUser, on_delete=models.CASCADE, verbose_name='To', related_name='to_sender')

    def __str__(self):
        return f'{self.receiver.first_name} {self.sender.last_name} Payment2'


class PaymentInfo(models.Model):
    detail = models.TextField(max_length=1000, verbose_name='Payment Information', blank=True, null=True)
    fee = models.DecimalField(max_digits=19, decimal_places=2, verbose_name='Transaction Fee', default=0.00)
    payment_info = models.ForeignKey(SentPayment, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.detail} Info'