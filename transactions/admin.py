from django.contrib import admin
from .models import SentPayment, ReceivedPayment, PaymentInfo


admin.site.register(SentPayment)
admin.site.register(ReceivedPayment)
admin.site.register(PaymentInfo)
