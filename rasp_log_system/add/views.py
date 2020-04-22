from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from datetime import datetime
import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from login.models import Login
from home.models import Raspberry
sys.path.insert(0, current_dir)

# Create your views here.
def add(request):
    #Teste se existe algum usuário conectado
    #para o ip atual
    l = get_logged_user(request)
    if isinstance(l, bool):
        return HttpResponseRedirect('/')

    #Dispositivos para usuário atual
    devices = get_devices(l)

    send_dict = {
        #Botão selecionado
       'btn_first': 3,
       'devices': devices,
    }

    return render(request, 'add.html', send_dict)

def add_device(request):
    #Teste se existe algum usuário conectado
    #para o ip atual
    l = get_logged_user(request)
    if isinstance(l, bool):
        return HttpResponseRedirect('/')

    #Info de post
    nome = request.POST['nome']
    ip = request.POST['ip']
    vers_snmp = request.POST['vers_snmp']
    community = request.POST['community']

    Raspberry.add_raspberry(l.username, nome, ip, vers_snmp, community)

    return HttpResponseRedirect('/add/')

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

def get_devices(login):
    devices_list = []
    for rasp in Raspberry.objects.all():
        if login.username in rasp.logins:
            devices_list.append(rasp)
    return devices_list

