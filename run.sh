#!/bin/sh

interface=""
firmware=""
root="/root"
attempts=0
timeout=0

if [ -f "$root/state" ]; then
    rm $root/state
    exit 0
fi

ip link set $interface down
sleep 5
ip link set $interface up

while true; do
    
    pppwn --interface "$interface" --fw "$firmware" --stage1 $root/offsets/stage1_$firmware.bin --stage2 $root/offsets/stage2_$firmware.bin --timeout $timeout --auto-retry

    if [ $? -eq 0 ]; then
        echo "Console attempts($attempts) PPPwned!" >> $root/state
        exit 0
    else
        attempts=$((attempts+1))
        ip link set $interface down
        sleep 5
        ip link set $interface up
    fi
    
done