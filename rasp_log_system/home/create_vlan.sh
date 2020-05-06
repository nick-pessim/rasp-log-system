#!/bin/bash

#Cria vlans em ambientes linux

#$1 - usuario
#$2 - ip
#$3 - senha
#$4 - interface_fis
#$5 - interface_vir
sshpass -p "$3" ssh $1@$2 "sudo vconfig add $4 $5"
sshpass -p "$3" ssh $1@$2 "sudo ip link set up $4.$5"
