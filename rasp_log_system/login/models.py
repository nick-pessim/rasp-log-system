from django.db import models
import os
from datetime import datetime
from cryptography.fernet import Fernet

# Create your models here.
class Login(models.Model):
    username = models.TextField()
    password = models.BinaryField()
    login_time = models.DateTimeField()
    is_logged = models.BooleanField()

    def login(username, password):
        #load cryptography
        key_file = open('login/key.key', 'rb')
        key = key_file.read()
        key_file.close()

        l = Login()
        for login in Login.objects.all():
            if login.username == username:
                #decrypt password
                f = Fernet(key)
                password_dec = f.decrypt(login.password)
                password_dec = password_dec.decode()
                if password_dec == password:
                    #change is_logged
                    Login.objects.filter(username=username).update(is_logged=True)
                    l = Login.objects.get(username=username)
                    return l
        return False

    def logout(self):
        Login.objects.filter(pk=Login.objects.get(id=self.id).pk).update(is_logged=False)

    def create(username, password):
        #load cryptography
        encrypt_file = open('login/key.key', 'rb')
        key = encrypt_file.read()
        encrypt_file.close()

        #encrypt password
        password = password.encode()
        f = Fernet(key)
        password = f.encrypt(password)

        l = Login(username=username, password=password, login_time=datetime.now(), is_logged=False)
        l.save()
