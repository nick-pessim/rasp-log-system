import json
import os
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

        #oids para display
        oid_nome = '1.3.6.1.2.1.1.5.0'
        oid_inst = '1.3.6.1.2.1.1.6.0'
        oid_syst = '1.3.6.1.2.1.1.1.0'
        oid_mac = '1.3.6.1.2.1.2.2.1.6.2' #mac da interface local, pode variar
        oid_interf = '1.3.6.1.2.1.25.3.2.1.3.262145'
        oid_vlan = '0'

        if nome == "0" or ip == "0" or vers_snmp == "0" or community == "0":
            nome_snmp = '-'
            inst_snmp = '-'
            syst_snmp = '-'
            mac_snmp = '-'
            interf_snmp = '-'
            vlan_snmp = '-'
        else:
            nome_snmp = snmpget_string(vers_snmp, community, ip, oid_nome)
            inst_snmp = snmpget_string(vers_snmp, community, ip, oid_inst)
            syst_snmp = snmpget_string(vers_snmp, community, ip, oid_syst)
            mac_snmp = snmpget_string(vers_snmp, community, ip, oid_mac)
            interf_snmp = snmpget_string(vers_snmp, community, ip, oid_interf)
            vlan_snmp = snmpget_string(vers_snmp, community, ip, oid_vlan)

        self.send(text_data=json.dumps({
            'nome_snmp': nome_snmp,
            'inst_snmp': inst_snmp,
            'syst_snmp': syst_snmp,
            'mac_snmp': mac_snmp,
            'interf_snmp': interf_snmp,
            'vlan_snmp': vlan_snmp,
        }))

#Enviar pacote snmp
def snmpget_string(vers_snmp, community, ip, oid):
    response = os.popen("snmpget -v " +str(vers_snmp) +" -c " +str(community) +" " +str(ip) +" " +str(oid)).read()
    oid = oid.replace("1", "iso", 1)
    if "Hex" not in response:
        response = response.replace(oid +" = STRING: ", "")
    else:
        response = response.replace(oid +" = Hex-STRING: ", "")
    response = response.replace("\"", "")
    return response
