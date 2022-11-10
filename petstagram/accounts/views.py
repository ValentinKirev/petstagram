from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from petstagram.accounts.forms import UserCreateForm, LoginForm

UserModel = get_user_model()


class SignUpView(CreateView):
    template_name = 'accounts/register-page.html'
    model = UserModel
    form_class = UserCreateForm
    success_url = reverse_lazy('login user')


class SignInView(LoginView):
    template_name = 'accounts/login-page.html'
    form_class = LoginForm


class SignOutView(LogoutView):
    pass


def details_user(request, pk):
    return render(request, 'accounts/profile-details-page.html')


def edit_user(request, pk):
    return render(request, 'accounts/profile-edit-page.html')


def delete_user(request, pk):
    return render(request, 'accounts/profile-delete-page.html')
