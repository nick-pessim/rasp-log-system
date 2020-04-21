from django.db import models
import os
import re

# Create your models here.
class Raspberry(models.Model):
    nome = models.TextField()
    ip = models.GenericIPAddressField()
    vers_snmp = models.TextField()
    community = models.TextField()

    #Necessário instalação de novas configurações de OID,
    #assim como a instalação dos pacotes snmp e snmpd
    def snmpget_pin_temperature(self):
       response = os.popen("snmpget -v " +self.vers_snmp +" -c " +self.community +" " +str(self.ip) +" 1.3.6.1.4.1.54392.5.118").read()
       response = response.replace("iso.3.6.1.4.1.54392.5.118 = STRING: ", "")
       response = re.findall("\d+\.\d+", response)[0]
       return float(response)
