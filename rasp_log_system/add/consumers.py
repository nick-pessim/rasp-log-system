import json
import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from home.models import Raspberry
sys.path.insert(0, current_dir)
from channels.generic.websocket import WebsocketConsumer

class OnlineRaspCheck(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        nome = text_data_json['nome']
        ip = text_data_json['ip']
        vers_snmp = text_data_json['vers_snmp']
        community = text_data_json['community']
        
        #get raspberry 
        r = Raspberry(nome = nome, ip = ip, vers_snmp = vers_snmp, community = community)

        if nome == "0" or ip == "0" or vers_snmp == "0" or community == "0":
            nome_snmp = '-'
            inst_snmp = '-'
            syst_snmp = '-'
            mac_snmp = '-'
            interf_snmp = '-'
            vlan_snmp = '-'
        else:
            nome_snmp = r.snmpget_by_descr('sysName', str)
            inst_snmp = r.snmpget_by_descr('sysLocation', str)
            syst_snmp = r.snmpget_by_descr('sysDescr', str)
            mac_snmp = r.snmpget_by_descr('macAddr', str)
            interf_snmp = r.snmpget_by_descr('interfNames', str)
            vlan_snmp = '-'

        self.send(text_data=json.dumps({
            'nome_snmp': nome_snmp,
            'inst_snmp': inst_snmp,
            'syst_snmp': syst_snmp,
            'mac_snmp': mac_snmp,
            'interf_snmp': interf_snmp,
            'vlan_snmp': vlan_snmp,
        }))

