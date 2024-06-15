import string
import random
from django.conf import settings
from apps.account.models import UserAccountActivation


def generate_activation_key(user, size=20):
    key = string.ascii_letters + string.digits
    final_key = ""
    for _ in range(size):
        final_key += random.choice(key)
    UserAccountActivation.objects.create(email=user.email, key=final_key)
    return final_key


def send_email_activation(user, request):
    """
    user: user object
    request: wsgi request object from views
    """
    key = generate_activation_key(user)
    final_url = f"http://127.0.0.1:8000/account/activate/{user.username}/{key}/"

    subject = "User Account Activation"
    message = f"""
    Please activate the account using the link provided
    {final_url}
    """
    user.email_user(subject=subject, message=message, from_email=settings.FROM_EMAIL)