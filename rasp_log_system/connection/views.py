from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .models import Connection
#common imports
from datetime import datetime
import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from login.models import Login
from home.models import Raspberry
sys.path.insert(0, current_dir)

# Create your views here.
def add_device_gateway(request, dev_name=""):
    #Teste se existe algum usuário conectado
    #para o ip atual
    l = get_logged_user(request)
    if isinstance(l, bool):
        return HttpResponseRedirect('/')

    #Dispositivos para usuário atual
    devices = get_devices(l)

    #Dispositivo escolhido
    r = None
    for dev in devices:
        if dev.nome == dev_name:
            r = dev
    
    #Conexão para dispositivo atual
    c = None
    if r != None:
        for con in Connection.objects.all():
            if con.ip == r.gateway:
                c = con

    send_dict = {
        #Botão selecionado
        'btn_first': 2,
        'devices': devices,
        'rasp_chosen': r,
        'rasp_con': c,
    }    

    return render(request, 'connection.html', send_dict)

def add_connection(request, dev_name=""):
    #Teste se existe algum usuário conectado
    #para o ip atual
    l = get_logged_user(request)
    if isinstance(l, bool):
        return HttpResponseRedirect('/')

    #Dispositivos para usuário atual
    devices = get_devices(l)

    #Dispositivo escolhido
    r = None
    for dev in devices:
        if dev.nome == dev_name:
            r = dev

    if r == None:
        return HttpResponseRedirect('/connection/')
    else:
        c = Connection(ip=r.gateway, nome=request.POST['nome'], password=request.POST['pass'], enable=request.POST['enable'], community=request.POST['community'], vers_snmp=request.POST['vers_snmp'])
        c.save()
        return HttpResponseRedirect('/connection/'+dev_name+'/')

def reset_connection(request, dev_name=""):
    #Teste se existe algum usuário conectado
    #para o ip atual
    l = get_logged_user(request)
    if isinstance(l, bool):
        return HttpResponseRedirect('/')

    #Dispositivos para usuário atual
    devices = get_devices(l)

    #Dispositivo escolhido
    r = None
    for dev in devices:
        if dev.nome == dev_name:
            r = dev
    
    if r == None:
        return HttpResponseRedirect('/connection/')

    #Conexao escolhida
    c = None
    for con in Connection.objects.all():
        if con.ip == r.gateway:
            con.delete()
    return HttpResponseRedirect('/connection/'+dev_name+'/')

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
