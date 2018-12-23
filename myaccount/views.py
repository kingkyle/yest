import qrcode
import qrcode.image.svg
from datetime import date, timedelta, datetime
from django.shortcuts import render, HttpResponse, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from qrcode.image.pure import PymagingImage
from django.utils.six import BytesIO
from .forms import (
    CheckEmailForm,
    EmailNotificationForm,
    PaymentInfoForm,
    PaymentAmountForm
    )
from .models import Balance, Card, Notifier, NotifierCount
from users.models import MyUser, Address
from transactions.models import SentPayment, ReceivedPayment, PaymentFee
from django.views.generic.edit import CreateView
from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


@login_required
def get_notifier(request):
    user = request.user
    notifiers = Notifier.objects.filter(user=user).order_by('-date')[:5]
    return notifiers


@login_required
def get_notifier_count(request):
    user = request.user
    counter = NotifierCount.objects.get(user=user)
    return counter


@login_required
def get_all_transactions(request):
    user = request.user
    sent = SentPayment.objects.filter(sender=user)
    received = ReceivedPayment.objects.filter(receiver=user)
    transactions = sent.union(received)
    return transactions


def filter_transaction_start_date(request, start_date):
    user = request.user
    sent = SentPayment.objects.filter(sender=user, date__gte=start_date)
    received = ReceivedPayment.objects.filter(receiver=user,
                                              date__gte=start_date)
    transactions = sent.union(received)
    return transactions


def filter_transaction_start_and_end(request, startdate, enddate, transtype):
    user = request.user
    if transtype == 'All':
        sent = SentPayment.objects.filter(sender=user,
                                          date__range=(startdate, enddate))
        received = ReceivedPayment.objects.filter(receiver=user,
                                                  date__range=(startdate,
                                                               enddate))
    else:
        sent = SentPayment.objects.filter(sender=user, trans_type=transtype,
                                          date__range=(startdate, enddate))
        received = ReceivedPayment.objects.filter(receiver=user,
                                                  trans_type=transtype,
                                                  date__range=(startdate,
                                                               enddate))
    transactions = sent.union(received)
    return transactions


def filter_transaction_duration(request, startdate, enddate, transtype):
    user = request.user
    if transtype == 'All':
        sent = SentPayment.objects.filter(sender=user,
                                          date__range=(startdate, enddate))
        received = ReceivedPayment.objects.filter(receiver=user,
                                                  date__range=(startdate,
                                                               enddate))
    else:
        sent = SentPayment.objects.filter(sender=user, trans_type=transtype,
                                          date__range=(startdate, enddate))
        received = ReceivedPayment.objects.filter(receiver=user,
                                                  trans_type=transtype,
                                                  date__range=(startdate,
                                                               enddate))
    transactions = sent.union(received)
    return transactions


@login_required
def home(request):
    notifiers = get_notifier(request)
    counter = get_notifier_count(request)
    transactions = get_all_transactions(request).order_by('-date')[:10]
    context = {
        'notifiers': notifiers,
        'counter': counter,
        'transactions': transactions
    }
    return render(request, 'myaccount/home.html', context)


@login_required
def resetCount(request):
    user = request.user
    notifier = NotifierCount.objects.filter(user=user).update(counter=0)
    return notifier


@login_required
def trans_details(request, trans_id):
    user = request.user
    sent = SentPayment.objects.filter(sender=user, trans_id=trans_id)
    received = ReceivedPayment.objects.filter(receiver=user, trans_id=trans_id)
    transaction = sent.union(received).filter(trans_id=trans_id)
    context = {
        'transaction': transaction
    }
    return render(request, 'myaccount/trans-detail.html', context)


@login_required
def all_transactions(request):
    end_date = date.today()
    start_date = date.today() - timedelta(days=30)
    page = request.GET.get('page', 1)
    transactions_list = filter_transaction_start_date(request, start_date)\
        .order_by('-date')
    paginator = Paginator(transactions_list, 10)
    try:
        transactions = paginator.page(page)
    except PageNotAnInteger:
        transactions = paginator.page(1)
    except EmptyPage:
        transactions = paginator.page(paginator.num_pages)
    context = {
        "end_date": end_date.strftime("%d-%m-%Y"),
        "start_date": start_date.strftime("%d-%m-%Y"),
        "transactions": transactions,
        "page_num": paginator.num_pages
    }
    return render(request, 'myaccount/all-transactions.html', context)


@login_required
def find_transaction(request, start_date, end_date, transtype):
    startdate = datetime.strptime(start_date, '%d-%m-%Y')
    enddate = datetime.strptime(end_date, '%d-%m-%Y')
    if request.is_ajax():
        transactions = filter_transaction_start_and_end(request, startdate,
                                                        enddate, transtype)\
            .order_by('-date')[:20]
        context = {
            "transactions": transactions
        }
    return render(request, 'myaccount/includes/trans-table.html', context)


@login_required
def duration_transaction(request, duration, transtype):
    startdate = date.today() - timedelta(days=duration)
    enddate = date.today()
    if request.is_ajax():
        transactions = filter_transaction_duration(request, startdate,
                                                   enddate, transtype)\
            .order_by('-date')[:5]
        context = {
            "transactions": transactions
        }
    return render(request, 'myaccount/includes/trans-table.html', context)


@login_required
def wallet(request):
    return render(request, 'myaccount/wallet.html')


class CardCreateView(LoginRequiredMixin, CreateView):
    model = Card
    fields = [
        'card_no', 'card_type', 'exp_date', 'security_code', 'billing_address'
    ]

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()

        form = super(CardCreateView, self).get_form(form_class)
        form.fields['exp_date'].widget = forms.TextInput(
            attrs={'placeholder': 'MM/YY'})
        return form

    def form_valid(self, form):
        form.instance.ccards = self.request.user
        return super().form_valid(form)


@login_required
def index(request):
    return redirect('myaccount-home')


@login_required
def send(request):
    try:
        del request.session['check_user']
    except KeyError:
        pass
    if request.method == 'POST':
        form = CheckEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['check_email'].lower()
            if email == request.user.email:
                messages.error(request, 'You cannot Send Payment To Yourself')
                return redirect('myaccount-send')
            else:
                check_user = MyUser.objects.filter(email__iexact=email).first()

                if check_user:
                    request.session['check_user'] = check_user.email.lower()
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
    try:
        ruser = request.session['check_user']
    except KeyError:
        return redirect('myaccount-send')
    if request.method == 'POST':
        form = PaymentAmountForm(request.POST)
        form2 = PaymentInfoForm(request.POST)
        if form.is_valid() and form2.is_valid():
            ruser = request.session['check_user']
            suser = request.user
            amount = form.cleaned_data['amount']
            detail = form2.cleaned_data['info']

            getfee = PaymentFee.objects.first()
            fee = getfee.fee
            bal = request.user.balance.get_balance()
            if amount > bal:
                messages.error(
                    request, 'You cannot complete this Payment, Check Balance')

                return redirect('myaccount-send')

            get_receiver = MyUser.objects.get(email=ruser)

            newPaymentSent = SentPayment(
                amount=amount, sender=suser, receiver=get_receiver,
                info=detail, fee=fee)

            newPaymentSent.save()

            messages.success(request, 'Payment Sent Successfully')
            try:
                del request.session['check_user']
            except KeyError:
                pass
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
    return render(request, 'myaccount/settings.html', context)


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
