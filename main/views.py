from django.shortcuts import render, redirect
from users.forms import UserCreationForm


def index(request):
    return render(request, 'main/index.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main-login')
    else:
        form = UserCreationForm()
    context = {
        'title': 'Join Quote Today!',
        'form': form
    }
    return render(request, 'main/register.html', context)


def request_payment(request):
    return render(request, 'main/request.html')