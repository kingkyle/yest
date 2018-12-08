from django.contrib import admin
from .models import Notification, Balance, Card, Notifier, NotifierCount


class BalanceAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'available_balance', 'pending_balance']

    class Meta:
        model = Balance


# Register your models here.
admin.site.register(Balance, BalanceAdmin)
admin.site.register(Notification)
admin.site.register(Card)
admin.site.register(Notifier)
admin.site.register(NotifierCount)
