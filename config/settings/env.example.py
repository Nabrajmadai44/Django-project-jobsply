import os
from .base import *
DEBUG = True
ALLOWED_HOSTS = []
SECRET_KEY = ''

MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")

DATABASES = {}

EMAIL_HOST = ''
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = ''

FROM_EMAIL = ""