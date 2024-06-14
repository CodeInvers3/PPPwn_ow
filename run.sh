#!/bin/sh

interface=""
version=""
root="/root"
timeout=0
stage1=""
stage2=""

ip link set $interface down
sleep 5
ip link set $interface up

pppwn --interface "$interface" --fw "$version" --stage1 $stage1 --stage2 $stage2 --timeout $timeout --auto-retry

if [ $? -eq 0 ]; then
    echo "Console attempts($attempts) PPPwned!"
    if /etc/init.d/pppoe-server status | grep -q "inactive"; then
        /etc/init.d/pppoe-server start
    fi
    exit 0
else
    exit 1
fi