#!/bin/sh

interface=""
version=""
root="/root"
timeout=0

ip link set $interface down
sleep 5
ip link set $interface up

pppwn --interface "$interface" --fw "$version" --stage1 $root/offsets/stage1_$version.bin --stage2 $root/offsets/stage2_$version.bin --timeout $timeout --auto-retry

if [ $? -eq 0 ]; then
    echo "Console attempts($attempts) PPPwned!"
    exit 0
else
    exit 1
fi