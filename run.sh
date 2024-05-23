#!/bin/sh

INTERFACE=""
FIRMWARE=""

ip link set $INTERFACE down
sleep 5
ip link set $INTERFACE up

while true; do
    ret=$(pppwn --interface "$INTERFACE" --fw "$FIRMWARE" --stage1 "/root/offsets/stage1_$FIRMWARE.bin" --stage2 "/root/offsets/stage2_$FIRMWARE.bin" --auto-retry)
    if [ "$ret" -ge 1 ]; then
        echo "\n$ret\n" > /www/pppwn/state.txt
        echo -e "\nConsole PPPwned!\n" >> /www/pppwn/state.txt
        exit 0
    else
        COUNTNUM=$((COUNTNUM+1))
        echo -e "\nFailed retrying...\n" > /www/pppwn/state.txt
        ip link set $INTERFACE down
        sleep 5
        ip link set $INTERFACE up
    fi
done