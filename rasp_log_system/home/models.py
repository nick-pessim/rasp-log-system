from django.db import models
import re
import ast
#common imports
import os,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
from pathlib import Path

# Create your models here.
class Raspberry(models.Model):
    nome = models.TextField()
    password = models.TextField()
    ip = models.GenericIPAddressField()
    vers_snmp = models.TextField()
    community = models.TextField()
    logins = models.TextField()
    gateway = models.TextField()
    gateway.default = ""
    logins.default = ""
    
    #Necessário instalação de novas configurações de OID,
    #assim como a instalação dos pacotes snmp e snmpd
    def snmpget_by_descr(self, descr, ret_type):
       return Raspberry.snmpget(self.vers_snmp, self.community, self.ip, Raspberry.call_oid(descr), ret_type)

    def snmpget_by_oid(self, oid, ret_type):
        return Raspberry.snmpget(self.vers_snmp, self.community, self.ip, oid, ret_type)

    def add_raspberry(username, nome, password, ip_rasp, vers_snmp, community):
        #Caso exista algum raspberry com mesmas configurações

        for rasp in Raspberry.objects.all():
            if ip_rasp == rasp.ip and vers_snmp == rasp.vers_snmp and community == rasp.community and rasp.nome == nome and rasp.password == password:
                logins_rasp = rasp.logins+','+username
                Raspberry.objects.filter(ip=ip_rasp).update(logins=logins_rasp)
                return Raspberry.objects.get(ip=ip_rasp)

        r = Raspberry(nome=nome, password=password, ip=ip_rasp, vers_snmp=vers_snmp, community=community, logins=username)
        r.find_gateway()
        r.save()
        return r

    def create_vlan(self, interf):
        os.popen('bash '+current_dir+'/create_vlan.sh '+self.nome+' '+self.ip+' '+self.password+' '+interf.split('.')[0]+' '+interf.split('.')[1])
    
    def delete_vlan(self, interf):
        os.popen('bash '+current_dir+'/delete_vlan.sh '+self.nome+' '+self.ip+' '+self.password+' '+interf.split('.')[0]+' '+interf.split('.')[1])

    def find_gateway(self):
        #separa interfaces virtuais de fisicas
        interf = separate_interf_types(ast.literal_eval(self.snmpget_by_descr('interfNames', str)))
        #connection_interf seleciona interface que existe vlans configuradas
        connection_interf = interf['vir_interf'][0]
        connection_interf = connection_interf[0:connection_interf.find('.')]
        self.gateway = os.popen("bash "+current_dir+"/get_gateway.sh "+self.nome+" "+self.ip+" "+self.password+" "+connection_interf).read()


    def call_oid(oid_desc):
        oid_file = open(os.path.join(os.path.dirname(__file__), 'oids.txt'), 'r')
        str_read = oid_file.read()
        str_read = str_read.split('\n')
        for string in str_read:
            if oid_desc in string:
                string = string.split('=')
                if string[1][0] != '[':
                    return string[1]
                else:
                    string = string[1].split('!')
                    oid_number = string[0]
                    #condicao
                    string = string[1]              #separa a condicional
                    string = string.split(']')[0]   #restringe a condicional a uma palavra
                    #oid_number
                    final_oid = []
                    oid_buffer = ""
                    for ch in oid_number:
                        try:
                            int(ch)
                            oid_buffer += ch
                        except:
                            if ch == '.' or ch == ',':
                                final_oid.append(int(oid_buffer))
                                oid_buffer = ""
                    return {'cond': string, 'number': final_oid}
        return None

    def snmpget(vers_snmp, community, ip, oid, ret_type): #dict detects that is a list of oids
        if ret_type == str or ret_type == float:
            if isinstance(oid, str):
                response = os.popen("snmpget -v " +str(vers_snmp) +" -c " +str(community) +" " +str(ip) +" " +str(oid)).read()
                oid = oid.replace("1", "iso", 1)
                if "Hex" not in response:
                    response = response.replace(oid +" = STRING: ", "")
                else:
                    response = response.replace(oid +" = Hex-STRING: ", "")
                response = response.replace("\"", "")
                response = response.replace("\n", "")
                if ret_type == float:
                    response = float(response)
                return response
            elif isinstance(oid, dict):
                response = []                                               #hold dict with response and corresponding oid
                response_buffer = oid['cond']                               #enter in a do-while loop
                i = 0                                                       #iterate oid
                while oid['cond'] in response_buffer:                       #send snmpget and analyze if response has conditional string
                    oid_buffer = ""
                    for num in oid['number']:                               #create string oid
                        oid_buffer+=str(num) +'.'
                    oid_buffer = oid_buffer[:len(oid_buffer)-1]             #remove last dot
                    response_buffer = os.popen("snmpget -v " +str(vers_snmp) +" -c " +str(community) +" " +str(ip) +" " +str(oid_buffer)).read()
                    if oid['cond'] in response_buffer:                      #append if condition exists in response
                        response.append({'ret': response_buffer, 'oid':oid_buffer})
                    oid['number'][len(oid['number'])-1]+=1                  #iterate oid to the next one
                full_ret = []
                for resp in response:                                       #remove irrevelevant part
                    resp['oid'] = resp['oid'].replace("1", "iso", 1)
                    if "Hex" not in resp['oid']:
                        resp['ret'] = resp['ret'].replace(resp['oid'] +" = STRING: ", "")
                    else:
                        resp['ret'] = resp['ret'].replace(resp['oid'] +" = Hex-STRING: ", "")
                    resp['ret'] = resp['ret'].replace("\"", "")
                    resp['ret'] = resp['ret'].replace("\n", "")
                    resp['ret'] = resp['ret'].replace(oid['cond'], "")      #remove condition detected
                    if ret_type == float:
                        resp['ret'] = float(resp['ret'])
                    full_ret.append(resp['ret'])
                return str(full_ret)

def separate_interf_types(interf_list):
    fis_interf = []
    vir_interf = []
    for interf in interf_list:
        if '.' in interf:               #interfaces virtuais em ambientes linux sao representados pela interface fisica.vlan_id
            vir_interf.append(interf)
        else:
            fis_interf.append(interf)
    return {'fis_interf': fis_interf, 'vir_interf': vir_interf}
