from django.contrib import admin
from .models import SentPayment, ReceivedPayment, PaymentFee


admin.site.register(SentPayment)
admin.site.register(ReceivedPayment)
admin.site.register(PaymentFee)
