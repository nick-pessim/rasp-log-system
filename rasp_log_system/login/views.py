from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .models import Login
#cryptography
from cryptography.fernet import Fernet
from datetime import datetime

# Create your views here.
def login(request):
    #Teste se existe algum usuário conectado
    #para o ip atual
    l = get_logged_user(request)
    if isinstance(l, Login):
        return HttpResponseRedirect('/home/')

    return render(request, 'login.html')

def logging(request):
    username = request.POST['username']
    password = request.POST['password']
    
    l = Login.login(username, password, request)

    return HttpResponseRedirect('/home/')

#Funções para sempre serem copiadas
def visitor_ip_address(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_logged_user(request):
    for l in Login.objects.all():
        if l.login_ip == visitor_ip_address(request) and ((datetime.now() - l.login_time).seconds/3600) < 3 and l.is_logged == True:
            return l
    return False
