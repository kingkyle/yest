from django.shortcuts import render, redirect
from users.forms import UserCreationForm
from users.models import MyUser, Profile
from .forms import UserCreationProfileForm


def index(request):
    return render(request, 'main/index.html')


def register(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            return redirect('myaccount-home')
        form = UserCreationForm(request.POST)
        form2 = UserCreationProfileForm(request.POST)
        if form.is_valid() and form2.is_valid():
            form.save()
            email = form.cleaned_data['email']
            country = form2.cleaned_data['country']
            phone = form2.cleaned_data['phone']
            user = MyUser.objects.get(email=email)
            Profile.objects.create(country=country, phone=phone, user=user)
            return redirect('main-login')
    else:
        if request.user.is_authenticated:
            return redirect('myaccount-home')
        form = UserCreationForm()
        form2 = UserCreationProfileForm()
    context = {
        'title': 'Join Quote Today!',
        'form': form,
        'form2': form2
    }
    return render(request, 'main/register.html', context)


def request_payment(request):
    return render(request, 'main/request.html')