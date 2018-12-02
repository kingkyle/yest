from django.db.models.signals import post_save
from transactions.models import SentPayment, ReceivedPayment
from users.models import MyUser, Profile
from .models import Balance
from django.dispatch import receiver


@receiver(post_save, sender=SentPayment)
def ReceiveSentPayment(sender, created, instance, **kwargs):
    if created:
        print(instance.receiver.pk)
        print(instance.sender.get_full_name())

        received = instance.receiver.pk
        sent = instance.sender.pk
        amount = instance.amount
        trans_id = instance.trans_id
        date = instance.date
        status = instance.status
        typed = 'Payment From'

        ReceivedPayment.objects.create(receiver_id=received, sender_id=sent, amount=amount, trans_id=trans_id, date=date, status=status, type=typed)


@receiver(post_save,sender=SentPayment)
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
def CreateProfile(sender, created, instance, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=MyUser)
def SaveProfile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_save, sender=MyUser)
def CreateBalance(sender, created, instance, **kwargs):
    if created:
        Balance.objects.create(user=instance)

