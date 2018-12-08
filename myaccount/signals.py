from django.db.models.signals import post_save
from transactions.models import SentPayment, ReceivedPayment
from users.models import MyUser, Profile
from .models import Balance, Notifier, NotifierCount
from django.dispatch import receiver


@receiver(post_save, sender=SentPayment)
def ReceiveSentPayment(sender, created, instance, **kwargs):
    if created:

        received = instance.receiver
        sent = instance.sender
        amount = instance.amount
        trans_id = instance.trans_id
        date = instance.date
        status = instance.status
        info = instance.info
        typed = 'Payment From'
        fee = instance.fee
        f_amount = amount-fee

        ReceivedPayment.objects.create(receiver=received, sender=sent, amount=f_amount, trans_id=trans_id, date=date,
                                       status=status, type=typed, info=info, fee=fee)


@receiver(post_save, sender=SentPayment)
def SentPaymentNotifier(sender, created, instance, **kwargs):
    if created:
        received = instance.receiver
        amount = instance.amount
        message = f'Money Received - {amount} USD'
        trans_id = instance.trans_id

        Notifier.objects.create(user=received, message=message, trans_id=trans_id)
        NotifierCount.objects.filter(user=received).update(counter=+1)


@receiver(post_save, sender=SentPayment)
def UpdateBalance(sender, created, instance, **kwargs):
    if created:
        received = instance.receiver.pk
        sent = instance.sender.pk
        amount = instance.amount

        ruser = MyUser.objects.get(id=received)
        suser = MyUser.objects.get(id=sent)

        rgetbal = Balance.objects.get(user=ruser.pk)
        rbal = rgetbal.available_balance
        addrbal = rbal + amount

        sgetbal = Balance.objects.get(user=suser.pk)
        sbal = sgetbal.available_balance
        addsbal = sbal - amount

        Balance.objects.filter(user=ruser.pk).update(available_balance=addrbal)
        Balance.objects.filter(user=suser.pk).update(available_balance=addsbal)


@receiver(post_save, sender=MyUser)
def CreateBalance(sender, created, instance, **kwargs):
    if created:
        Balance.objects.create(user=instance)
        NotifierCount.objects.create(user=instance)

