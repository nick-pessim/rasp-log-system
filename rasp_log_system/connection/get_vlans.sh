#!/bin/bash

#Retorna as vlans existentes em roteadores

#$1 - snmp_vers
#$2 - community
#$3 - ip

NEXT=$(snmpgetnext -v$1 -c$2 $3 1.3.6.1.2.1.2.2.1.2.151060481)
OID=${NEXT%=*}
RETURN="Vlan1"
while [[ "$NEXT" == *"Vlan"* ]]
do
	if [[ "$NEXT" == *"Vlan"* ]];
        then
		NEXT=${NEXT//\"/$''}
                RETURN="$RETURN,${NEXT##*: }"
        fi
	NEXT=$(snmpgetnext -v$1 -c$2 $3 $OID)
	OID=${NEXT% =*}
done
echo $RETURN
