from django.contrib import admin
from django.urls import path
from . import views
from .forms import LoginForm, MyPasswordResetForm
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.ViewPoll, name="viewpoll"),
    path("create-polls/", views.CreatePoll, name="createpoll"),
    path("user-register/", views.UserRegistrationFormView.as_view(), name="userregister"),
    path("accounts/login/", auth_views.LoginView.as_view(template_name='app/userlogin.html', authentication_form=LoginForm), name="userlogin"),
    path('logout/', auth_views.LogoutView.as_view(next_page='userlogin'), name='userlogout'),
    path("accounts/profile/", views.UserProfile, name="userprofile"),
    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='app/userpasswordreset.html', form_class=MyPasswordResetForm), name='reset_password'),
]