from django.db import models
#common imports
import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)

# Create your models here.
class Connection(models.Model):
    ip = models.GenericIPAddressField()
    nome = models.TextField()
    password = models.TextField()
    enable = models.TextField()
    community = models.TextField()
    vers_snmp = models.TextField()

    def get_vlans(self):
        string_vlan = os.popen("bash "+current_dir+"/get_vlans.sh "+self.vers_snmp+" "+self.community+" "+self.ip).read()
        return string_vlan.split(',')
