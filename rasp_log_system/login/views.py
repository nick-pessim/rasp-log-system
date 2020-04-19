from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .models import Login
#cryptography
from cryptography.fernet import Fernet

# Create your views here.
def login(request):
    return render(request, 'login.html', {})

def logging(request):
    username = request.POST['username']
    password = request.POST['password']
    
    l = Login.login(username, password)

    return HttpResponse(str(l))
