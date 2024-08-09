from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.EmailField(primary_key=True)
    avatar = models.ImageField(upload_to="avatar/", null=True, blank=True)

    # Set email as None, because username itself is email
    email = None
    EMAIL_FIELD = "username"
    REQUIRED_FIELDS = []
