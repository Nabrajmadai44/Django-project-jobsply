import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.commons.models import DateTimeModel


class User(AbstractUser):
    username = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(max_length=50, unique=True)
    middle_name = models.CharField(max_length=50, null=True, blank=True)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]


class UserProfile(DateTimeModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.FileField(null=True, blank=True, upload_to="profile_pictures")
    phone = models.CharField(max_length=14)
    address = models.CharField(max_length=50)
    resume = models.FileField(null=True, blank=True, upload_to="resumes")
    bio = models.TextField(max_length=500)

    def __str__(self):
        return f"Profile of {self.user.email}"