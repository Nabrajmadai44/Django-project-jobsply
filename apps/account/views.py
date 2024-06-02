from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegisterForm, UserLoginForm


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