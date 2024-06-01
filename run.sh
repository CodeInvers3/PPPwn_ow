#!/bin/sh

interface=""
firmware=""
root="/root"
signalfile="/www/pppwn/stop"
attempts=0
timeout=0

ip link set $interface down
sleep 5
ip link set $interface up

while true; do
    
    if [ -f "$signalfile" ]; then

        echo "{\"stop\":true}" > "/www/pppwn/state.json"

        pids=$(pgrep pppwn)
        for pid in $pids; do
            kill $pid
        done

        if [ -f "$signalfile" ]; then
            rm $signalfile
        fi
        
        exit 1
    fi
    
    pppwn --interface "$interface" --fw "$firmware" --stage1 $root/offsets/stage1_$firmware.bin --stage2 $root/offsets/stage2_$firmware.bin --timeout $timeout --auto-retry
    
    if [ $? -eq 0 ]; then
        echo "Console attempts($attempts) PPPwned!" > $root/state
        exit 0
    else
        attempts=$((attempts+1))
        ip link set $interface down
        sleep 5
        ip link set $interface up
    fi
    
done