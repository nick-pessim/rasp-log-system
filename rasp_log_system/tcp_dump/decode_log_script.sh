#!/usr/bin/sh

#$1 - arquivo

tcpdump -r $1 > $2
