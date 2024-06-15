from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.views.generic import CreateView, FormView, View, DetailView
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegisterForm, UserLoginForm
from .utils import send_email_activation
from .models import UserAccountActivation

User = get_user_model()


class UserRegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = "account/user_register.html"
    # success_url = reverse_lazy("home_page")

    def form_valid(self, form):
        password1 = form.cleaned_data.pop("password1")
        form.cleaned_data.pop("password2")
        user = form.save()
        user.set_password(password1)
        user.save()
        send_email_activation(user, self.request)
        messages.success(self.request, "User created successfully!")
        return redirect("home_page")

    def form_invalid(self, form):
        messages.error(self.request, "Couldn't add user!")
        return super().form_invalid(form)


class UserLoginView(FormView):
    form_class = UserLoginForm
    template_name = "account/user_login.html"

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]
        user = authenticate(self.request, email=email, password=password)
        if user:
            login(self.request, user)
            messages.success(self.request, "User logged in!")
            return redirect("home_page")
        messages.error(self.request, "Invalid credentials!")
        return redirect("user_login")


def user_logout(request):
    logout(request)
    messages.success(request, "User logged out !")
    return redirect("home_page")


class UserAccountActivationView(View):
    def get(self, *args, **kwargs):
        username = kwargs["username"]
        key = kwargs["key"]
        user = User.objects.filter(username=username)
        if user.exists():
            user = user[0]
            ua = UserAccountActivation.objects.filter(key=key, email=user.email)
            if ua.exists():
                user.is_verified = True
                user.save()
                messages.success(self.request, "Account Activated !")
                return redirect("home_page")
        messages.error(self.request, "Invalid activation link !")
        return redirect("user_login")


class ResendEmailActivation(View):
    def get(self, *args, **kwargs):
        send_email_activation(self.request.user, self.request)
        messages.success(self.request, "Activation link resent !")
        return redirect("home_page")


class UserProfileView(DetailView):
    queryset = User.objects.all()
    template_name = "account/user_profile.html"