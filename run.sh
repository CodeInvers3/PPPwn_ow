#!/bin/sh

interface=""
version=""
root="/root"
timeout=0
stage1=""
stage2=""

if /etc/init.d/pppoe-server status | grep -q "running"; then
    /etc/init.d/pppoe-server stop
fi

ip link set $interface down
sleep 5
ip link set $interface up

pppwn --interface "$interface" --fw "$version" --stage1 $stage1 --stage2 $stage2 --timeout $timeout --auto-retry

if [ $? -eq 0 ]; then
    if /etc/init.d/pppoe-server status | grep -q "inactive"; then
        /etc/init.d/pppoe-server start
    fi
    echo "Console attempts($attempts) PPPwned!\n" > "log"
    exit 0
else
    echo "Fail attempts($attempts)\n" > "log"
    exit 1
fi