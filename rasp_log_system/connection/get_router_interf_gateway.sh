#!/bin/bash

#Habilita vlan no tronco entre gateway e raspberry

#Gateway inputs
#$1 - vers_snmp
#$2 - community
#$3 - ip
#$4 - interf descr

OID_INTERF_DESCR="1.3.6.1.2.1.31.1.1.1.18"
OID_INTERF="1.3.6.1.2.1.2.2.1.2"

###Gateway
#1.3.6.1.2.1.31.1.1.1.18 - retorna descr das interfaces e isola codigo da interface
OID=$(snmpwalk -v$1 -c$2 $3 $OID_INTERF_DESCR | grep "$4")
OID=${OID% =*}
OID=${OID##*.}
OID="$OID_INTERF.$OID"
INTERF=$(snmpget -v$1 -c$2 $3 $OID -Ov)
INTERF=${INTERF//STRING: \"/$''}
INTERF=${INTERF//\"/$''}
echo $INTERF
