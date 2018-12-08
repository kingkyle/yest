from django import forms
from users.models import MyUser
from transactions.models import SentPayment
from .models import Notification


class CheckEmailForm(forms.Form):
    check_email = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Email Address of Receiver',
                                                                          'autocomplete': 'off'}))


class EmailNotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['send_payment', 'receive_payment', 'surveys', 'news', 'info_update',
                  'address_update', 'bank_update', 'card_update']
        widgets = {'send_payment': forms.CheckboxInput(attrs={'disabled': 'disabled'}),
                   'info_update': forms.CheckboxInput(attrs={'disabled': 'disabled'})}


class PaymentInfoForm(forms.ModelForm):
    class Meta:
        model = SentPayment
        fields = ['info']
        widgets = {'info': forms.Textarea(attrs={'placeholder': 'Enter Details About the Payment (Optional)'})}


class PaymentAmountForm(forms.ModelForm):
    class Meta:
        model = SentPayment
        fields = ['amount']
        widgets = {'amount': forms.NumberInput(attrs={'placeholder': '0.00'})}



