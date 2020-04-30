from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import ast #convert str list into list
#common imports
from datetime import datetime
import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from login.models import Login
from home.models import Raspberry
sys.path.insert(0, current_dir)
import mimetypes


# Create your views here.
def dump(request, dev_name=""):
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

    send_dict = {}
    if r != None:
        #separa interfaces virtuais de fisicas
        interf = separate_interf_types(ast.literal_eval(r.snmpget_by_descr('interfNames', str)))
        send_dict = {
            #Botão selecionado
            'btn_first': 4,
            'devices': devices,
            'rasp_chosen': r,
            'interfs_fis': interf['fis_interf'],    #para a combobox
            'interfs_vir': interf['vir_interf'],    #
        }
    else:
        send_dict = {
            #Botão selecionado
            'btn_first': 4,
            'devices': devices,
            'rasp_chosen': r,
            'interfs_fis': [], #ignore exception
            'interfs_vir': [], #
        }

    print(send_dict)

    return render(request, 'tcp_dump.html', send_dict)


def download_dump_file(request, dump_file=""):
    # fill these variables with real values
    fl_path = current_dir+"/logs/"+dump_file
    filename = dump_file

    fl = open(fl_path, 'rb')
    mime_type, _ = mimetypes.guess_type(fl_path)
    response = HttpResponse(fl, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response

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

def separate_interf_types(interf_list):
    fis_interf = []
    vir_interf = []
    for interf in interf_list:
        if '.' in interf:               #interfaces virtuais em ambientes linux sao representados pela interface fisica.vlan_id
            vir_interf.append(interf)
        else:
            fis_interf.append(interf)
    return {'fis_interf': fis_interf, 'vir_interf': vir_interf}
