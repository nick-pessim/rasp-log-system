#!/usr/bin/sh

#Retorna a interface conectada ao gateway4

#$1 - usuario
#$2 - ip
#$3 - senha
#$4 - gateway

INTERF=`sshpass -p "$3" ssh $1@$2 ip route | grep "default via" | grep "$4"`
INTERF=${INTERF% proto*}
INTERF=${INTERF##*dev }
INTERF=${INTERF%.*}
echo $INTERF
