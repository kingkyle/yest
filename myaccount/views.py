import qrcode
import qrcode.image.svg
from django.shortcuts import render, HttpResponse, redirect
from qrcode.image.pure import PymagingImage
from django.utils.six import BytesIO
from .forms import CheckEmailForm, EmailNotificationForm, PaymentInfoForm, PaymentAmountForm
from .models import Balance, Card
from users.models import MyUser, Address
from transactions.models import SentPayment, ReceivedPayment, PaymentInfo
from django.views.generic.edit import CreateView
from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


@login_required
def home(request):
    user = request.user
    sent = SentPayment.objects.filter(sender=user.pk)
    received = ReceivedPayment.objects.filter(sender=user.pk)
    transactions = sent.union(received).order_by('-date')[:10]
    context = {
        'user': user,
        'sent': sent,
        'received': received,
        'transactions': transactions
    }
    return render(request, 'myaccount/home.html', context)


class CardCreateView(LoginRequiredMixin, CreateView):
    model = Card
    fields = ['card_no', 'card_type', 'exp_date', 'security_code', 'billing_address']

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()

        form = super(CardCreateView, self).get_form(form_class)
        form.fields['exp_date'].widget = forms.TextInput(attrs={'placeholder': 'MM/YY'})
        return form

    def form_valid(self, form):
        form.instance.ccards = self.request.user
        return super().form_valid(form)


@login_required
def index(request):
    return redirect('myaccount-home')


@login_required
def send(request):
    if request.method == 'POST':
        form = CheckEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['check_email']
            if email == request.user.email:
                messages.error(request, 'You cannot Send Payment To Yourself')
                return redirect('myaccount-send')
            else:
                check_user = MyUser.objects.filter(email=email).first()

                if check_user:
                    request.session['check_user'] = check_user.email
                    return redirect('myaccount-send-info')
                else:
                    messages.error(request, 'No User With Such Email Found!')
                    return redirect('myaccount-send')
    else:
        form = CheckEmailForm()
    context = {
        'form': form
    }
    return render(request, 'myaccount/send.html', context)


@login_required
def send_info(request):
    if request.method == 'POST':
        form = PaymentAmountForm(request.POST)
        form2 = PaymentInfoForm(request.POST)
        if form.is_valid() and form2.is_valid():
            ruser = request.session['check_user']
            suser = request.user.email
            amount = form.cleaned_data['amount']
            detail = form2.cleaned_data['detail']

            bal = request.user.balance.get_balance()
            if amount > bal:
                messages.error(request, 'You cannot complete this Payment, Check Balance')
                return redirect('myaccount-send')

            rgetuser = MyUser.objects.filter(email=ruser).first()
            sgetuser = MyUser.objects.filter(email=suser).first()

            newPaymentSent = SentPayment(amount=amount, sender_id=sgetuser.pk, receiver_id=rgetuser.pk)
            newPaymentSent.save()

            newPaymentInfo =  PaymentInfo(detail=detail, payment_info_id=newPaymentSent.id)
            newPaymentInfo.save()

            messages.success(request, 'Payment Sent Successfully')
            return redirect('myaccount-send')
    else:
        form = PaymentAmountForm()
        form2 = PaymentInfoForm()
    context = {
        'form': form,
        'form2': form2,
        'check_user': request.session['check_user']
    }
    return render(request, 'myaccount/send-info.html', context)


@login_required
def receive(request):
    return render(request, 'myaccount/receive.html')


@login_required
def profile(request):
    return redirect('myaccount-settings')


@login_required
def settings(request):
    user = request.user
    context = {
        'user': user
    }
    return render(request, 'myaccount/settings.html')


@login_required
def payment(request):
    return render(request, 'myaccount/payment.html')


@login_required
def payment_info(request):
    return render(request, 'myaccount/payment-info.html')


@login_required
def notification(request):
    form = EmailNotificationForm()
    context = {
        'form': form
    }
    return render(request, 'myaccount/notifications.html', context)

@login_required
def qr_image(request):
    email = request.user.email
    data = f'email:{email}?amount='
    img = qrcode.make(data, image_factory=PymagingImage)
    Buf = BytesIO()
    img.save(Buf)
    image_stream = Buf.getvalue()
    response = HttpResponse(image_stream, content_type='image/jpg')
    response['Content-Disposition'] = 'inline; filename="qr.jpg"'
    return response

@login_required
def qr_amount(request, amount, detail):
    email = request.user.email
    data = f'email:{email}?amount={amount}?detail={detail}'
    img = qrcode.make(data, image_factory=PymagingImage)
    Buf = BytesIO()
    img.save(Buf)
    image_stream = Buf.getvalue()
    response = HttpResponse(image_stream, content_type='image/jpg')
    response['Content-Disposition'] = 'inline; filename="qr.jpg"'
    return response