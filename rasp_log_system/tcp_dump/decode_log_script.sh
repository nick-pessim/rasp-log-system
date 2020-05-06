#!/usr/bin/sh

#Decodifica arquivo pcap para visualizacao

#$1 - arquivo

tcpdump -r $1 > $2
