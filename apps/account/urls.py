from django.urls import path
from . import views


urlpatterns = [
    path("user-register", views.UserRegisterView.as_view(), name="user_register"),
    path("user-login", views.UserLoginView.as_view(), name="user_login")
]
