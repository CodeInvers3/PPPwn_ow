#!/bin/sh

INTERFACE="br-lan"
FIRMWAREVERSION="1100"

ip link set $INTERFACE down
sleep 5
ip link set $INTERFACE up

while true; do
    ret=$(pppwn --interface $INTERFACE --fw $FIRMWAREVERSION --stage1 ~/offsets/stage1_$FIRMWAREVERSION.bin --stage2 ~/offsets/stage2_$FIRMWAREVERSION.bin --auto-retry)
    if [ "$ret" -ge 1 ]; then
        echo "\n$ret\n" > ~/state.txt
        echo -e "\nConsole PPPwned!\n" >> ~/state.txt
        exit 0
    else
        COUNTNUM=$((COUNTNUM+1))
        echo -e "\nFailed retrying...\n" > ~/state.txt
        ip link set $INTERFACE down
        sleep 5
        ip link set $INTERFACE up
    fi
done
