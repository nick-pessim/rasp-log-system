from django.db import models
import os
#encrypt
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Create your models here.
class Login(models.Model):
    username = models.TextField()
    password = models.TextField()
    login_time = models.DateTimeField()
    is_logged = models.BooleanField()

    def login(self):
        Login.objects.filter(pk=Login.objects.get(id=self.id).pk).update(is_logged=True)

    def logout(self):
        Login.objects.filter(pk=Login.objects.get(id=self.id).pk).update(is_logged=False)
