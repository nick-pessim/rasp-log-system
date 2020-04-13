from django.shortcuts import render
from .models import Login

# Create your views here.
def login(request, msg_error=''):
    try:
        id_failed = int(msg_error[len(msg_error)-1])
    except:
        id_failed = 0
    return render(request, 'login.html', {'id_failed':id_failed})
