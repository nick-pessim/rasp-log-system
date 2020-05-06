import json
import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from home.models import Raspberry
from connection.models import Connection
sys.path.insert(0, current_dir)
from channels.generic.websocket import WebsocketConsumer
from datetime import datetime
from time import sleep

class tcp_dump_request(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        dev = json.loads(text_data)
        duracao = int(dev['duracao'])

        #Dispositivo escolhido
        r = None
        for device in Raspberry.objects.all():
            if dev['nome'] == device.nome and dev['senha'] == device.password and dev['ip'] == device.ip:
                r = device
        
        #Gateway do dispositivo
        c = None
        for con in Connection.objects.all():
            if r.gateway == con.ip:
                c = con
        
        #Prepara nomes dos arquivos
        file_name = "log_"+(dev['ip']).replace(".", "-")+"_"+dev['interf']+"_"+str(datetime.now()).replace(" ", "-")
        file_full_name = current_dir+"/logs/"+file_name+".pcap"
        file_decoded_name = current_dir+"/logs/decoded/"+file_name+".txt"
        
        #Retorna gateway da interface router
        dev['interf'] = dev['interf'].replace("Vlan","")
        dev['interf'] = os.popen('bash '+current_dir+'/get_interf_gateway.sh '+r.nome+' '+r.ip +' '+r.password+' '+r.gateway).read().replace("\n","")+'.'+dev['interf']
        
        #Cria configuracoes
        c.add_vlan_to_trunk(dev['interf'])
        r.create_vlan(dev['interf'])
        
        #Intervalo para atualizacao de informacoes
        sleep(2)

        #Comeca dump
        os.popen("bash "+current_dir+"/create_log_script.sh "+dev['nome']+" "+dev['ip']+" "+dev['senha']+" "+str(duracao)+" "+dev['interf']+" "+file_full_name)

        sleep(duracao+5)

        os.popen("bash "+current_dir+"/decode_log_script.sh "+file_full_name+" "+file_decoded_name)  #decoded file
        sleep(5)
        file_decoded = open(file_decoded_name, 'r')
        decoded = file_decoded.read()
        file_decoded.close()

        #Remove configuracoes
        c.remove_vlan_from_trunk(dev['interf'])
        r.delete_vlan(dev['interf'])


        self.send(text_data=json.dumps({
            'data': decoded,
            'pcap_file': file_name+".pcap",
        }))
