from django.db import models
import netmiko
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

    def add_vlan_to_trunk(self, vlan):
        interf_descr = os.popen('bash '+parent_dir+'/gateway_interf_descr.sh').read()
        interf = os.popen('bash '+current_dir+'/get_router_interf_gateway.sh '+self.vers_snmp+' '+self.community+' '+self.ip.replace('\n',"")+' '+interf_descr).read()
        device_type=""
        if self.enable == "":
            device_type='cisco_nxos'
        else:
            device_type='cisco_ios'
        self.connection = netmiko.ConnectHandler(ip=self.ip, device_type=device_type, username=self.nome, password=self.password, secret=self.enable)
        if self.enable == "":
            self.connection.enable()
        self.connection.config_mode()
        self.connection.send_command_timing("terminal length 0")
        self.connection.send_command_timing("interface "+interf)
        self.connection.send_command_timing("switchport trunk allowed vlan add "+vlan.split('.')[1])
        self.connection.send_command_timing("end\nexit")

    def remove_vlan_from_trunk(self, vlan):
        interf_descr = os.popen('bash '+parent_dir+'/gateway_interf_descr.sh').read()
        interf = os.popen('bash '+current_dir+'/get_router_interf_gateway.sh '+self.vers_snmp+' '+self.community+' '+self.ip.replace('\n',"")+' '+interf_descr).read()
        device_type=""
        if self.enable == "":
            device_type='cisco_nxos'
        else:
            device_type='cisco_ios'
        self.connection = netmiko.ConnectHandler(ip=self.ip, device_type=device_type, username=self.nome, password=self.password, secret=self.enable)
        if self.enable == "":
            self.connection.enable()
        self.connection.config_mode()
        self.connection.send_command_timing("terminal length 0")
        self.connection.send_command_timing("interface "+interf)
        self.connection.send_command_timing("switchport trunk allowed vlan remove "+vlan.split('.')[1])
        self.connection.send_command_timing("end\nexit")
