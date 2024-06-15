from django.contrib import admin
from apps.account.models import User, UserProfile


admin.site.register(User)
admin.site.register(UserProfile)