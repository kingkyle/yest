from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name="main-index"),
    path('login/', auth_views.LoginView.as_view(template_name='main/login.html', redirect_authenticated_user=True), name='main-login'),
    path('logout/', auth_views.LogoutView.as_view(), name='main-logout'),
    path('request/', views.request_payment, name='main-request'),
    path('register/', views.register, name='main-register')
]