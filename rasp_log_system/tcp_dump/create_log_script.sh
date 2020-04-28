#!/usr/bin/sh

#$1 - usuario
#$2 - ip
#$3 - senha
#$4 - duracao (s)
#$5 - interface
#$6 - arquivo

sshpass -p "$3" ssh $1@$2 tcpdump -G $4 -W 1 -U -s0 'not port 22' -i $5 -w -> $6
