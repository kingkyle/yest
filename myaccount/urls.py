from django.urls import path
from . import views
from .views import CardCreateView

urlpatterns = [
    path('home/', views.home, name='myaccount-home'),
    path('receive/', views.receive, name='myaccount-receive'),
    path('send/', views.send, name='myaccount-send'),
    path('send/send-info/', views.send_info, name='myaccount-send-info'),
    path('profile/settings/', views.settings, name='myaccount-settings'),
    path('profile/payment/', views.payment, name='myaccount-payment'),
    path('profile/payment-info/', views.payment_info, name='myaccount-payment-info'),
    path('profile/', views.profile, name='myaccount-profile'),
    path('profile/notification/', views.notification, name='myaccount-notification'),
    path('profile/add-card/', CardCreateView.as_view(), name='myaccount-add-card'),
    path('qr-image/', views.qr_image, name='myaccount-qr-image'),
    path('qr-image/<amount>/<detail>/', views.qr_amount, name='myaccount-qr-amount'),
    path('', views.index, name='myaccount-index')
]