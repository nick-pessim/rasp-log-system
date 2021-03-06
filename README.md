# Rasp Log System (RLS)

![Rasp-logo](https://raw.github.com/nick-pessim/rasp-log-system/master/logo.png)

Este repositório tem como objetivo construir uma interface online na linguagem python utilizando o Django para acesso http de uma raspberry-pi, via webserver em linux, e retirar informações assim como fazer com que ela edite configurações locais. As requisições serão feitas via snmp.

Pré-requisitos:
-	Instalação pacote snmp e snmpd
-	Edição do arquivo snmpd.conf para aceitar determinadas oid's

Instruções para edição do snmpd.conf:
1.	Criar arquivo bash em *script_location* que print a informação desejada, sugestão: usar o cat
	ex: 
```bash
    #!/bin/bash
    if [ "$1" = "-g" ]
    then
    echo *oid*
    echo string
    cat *arquivo_info*
    fi
    exit 0
```

2.	Adicionar OID nas configurações do snmpd.conf
	ex:
```bash
	pass *oid* /bin/sh  *script_location*
```

3.	Dar os restart nas configurações snmpd.conf
```bash
	/etc/init.d/snmp restart
```
