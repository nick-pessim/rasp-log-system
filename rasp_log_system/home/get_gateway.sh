#!/usr/bin/sh

#Retorna o gateway4 da interface selecionada

#$1 - usuario
#$2 - ip
#$3 - senha
#$4 - interface

echo `sshpass -p "$3" ssh $1@$2 ip route | grep "default via" | grep "$4" | grep -oE "\b([0-9]{1,3}\.){3}[0-9]{1,3}\b"`
