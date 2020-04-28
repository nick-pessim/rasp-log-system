import json
import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from home.models import Raspberry
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
        duracao = int(dev['duracao'])*60 #minutos

        file_name = "log_"+(dev['ip']).replace(".", "-")+"_"+dev['interf']+"_"+str(datetime.now()).replace(" ", "-")
        file_full_name = current_dir+"/logs/"+file_name+".pcap"
        file_decoded_name = current_dir+"/logs/decoded/"+file_name+".txt"

        os.popen("bash "+current_dir+"/create_log_script.sh "+dev['nome']+" "+dev['ip']+" "+dev['senha']+" "+str(duracao)+" "+dev['interf']+" "+file_full_name)

        sleep(duracao+5)

        os.popen("bash "+current_dir+"/decode_log_script.sh "+file_full_name+" "+file_decoded_name)  #decoded file
        sleep(5)
        file_decoded = open(file_decoded_name, 'r')
        decoded = file_decoded.read()
        file_decoded.close()

        self.send(text_data=json.dumps({
            'data': decoded,
            'pcap_file': file_name+".pcap",
        }))
