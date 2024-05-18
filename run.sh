#!/bin/sh

INTERFACE="br-lan"
FIRMWAREVERSION="750"
COUNTNUM=0
ATTEMPTSMAX=5

ip link set $INTERFACE down
sleep 5
ip link set $INTERFACE up

while true; do
    ret=$(/root/pppwn --interface $INTERFACE --fw $FIRMWAREVERSION --stage1 /root/stage1_$FIRMWAREVERSION.bin --stage2 /root/stage2_$FIRMWAREVERSION.bin --auto-retry)
    if [ "$COUNTNUM" -eq "$ATTEMPTSMAX" ]; then
    break
    fi
    if [ "$ret" -ge 1 ]; then
        echo "\n$ret\n" > /root/state.txt
        echo -e "\nConsole PPPwned!\n" >> /root/state.txt
        break
    else
        COUNTNUM=$((COUNTNUM+1))
        echo -e "\nFailed retrying...\n" > /root/state.txt
        ip link set $INTERFACE down
        sleep 5
        ip link set $INTERFACE up
    fi
done
