from django.db import models
import os
import re

# Create your models here.
class Raspberry(models.Model):
    nome = models.TextField()
    ip = models.GenericIPAddressField()
    vers_snmp = models.TextField()
    community = models.TextField()
    logins = models.TextField()
    logins.default = ""

    #Necessário instalação de novas configurações de OID,
    #assim como a instalação dos pacotes snmp e snmpd
    def snmpget_pin_temperature(self):
       return snmpget_float(self.vers_snmp, self.community, self.ip, "1.3.6.1.4.1.54392.5.118")

    def add_raspberry(username, nome, ip_rasp, vers_snmp, community):
        #Caso exista algum raspberry com mesmas configurações
        for rasp in Raspberry.objects.all():
            if ip_rasp == rasp.ip and vers_snmp == rasp.vers_snmp and community == rasp.community:
                logins_rasp = rasp.logins+','+username
                Raspberry.objects.filter(ip=ip_rasp).update(logins=logins_rasp)
                return Raspberry.objects.get(ip=ip_rasp)
        
        r = Raspberry(nome=nome, ip=ip_rasp, vers_snmp=vers_snmp, community=community, logins=username)
        r.save()
        return r

#Enviar pacote snmp
def snmpget_float(vers_snmp, community, ip, oid):
    response = os.popen("snmpget -v " +vers_snmp +" -c " +community +" " +str(ip) +" " +oid).read()
    oid = oid.replace("1", "iso", 1)
    response = response.replace(oid +" = STRING: ", "")
    response = re.findall("\d+\.\d+", response)[0]
    return float(response)
