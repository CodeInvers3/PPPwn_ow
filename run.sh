#!/bin/sh

INTERFACE="br-lan" # Aquí el nombre de la interface de ethernet
FIRMWAREVERSION="750" #colocar aquí la version del firmware
SHUTDOWN=true
USBETHERNET=false

echo -e "\n\n _____  _____  _____"
echo "|  __ \\|  __ \\|  __ \\"
echo "| |__) | |__) | |__) |_      ___ __"
echo "|  ___/|  ___/|  ___/\\ \\ /\\ / / '_ \\"
echo "| |    | |    | |     \\ V  V /| | | |"
echo "|_|    |_|    |_|      \\_/\\_/ |_| |_|"
echo -e "\nhttps://github.com/TheOfficialFloW/PPPwn\n"

if [ "$USBETHERNET" = "true" ]; then
    echo '1-1' > /sys/bus/usb/drivers/usb/unbind
    sleep 2
    echo '1-1' > /sys/bus/usb/drivers/usb/bind
    sleep 5
else
    ifconfig $INTERFACE down
    sleep 5
fi
ifconfig $INTERFACE up

echo -e "\nReady for console connection\nFirmware: $FIRMWAREVERSION\nInterface: $INTERFACE\n"

while true; do
    ret=$(/root/pppwn --interface $INTERFACE --fw $FIRMWAREVERSION --stage1 /root/stage1_$FIRMWAREVERSION.bin --stage2 /root/stage2_$FIRMWAREVERSION.bin --auto-retry)
    if [ "$ret" -ge 1 ]; then
        echo -e "\nConsole PPPwned!\n"
        if [ "$SHUTDOWN" = "true" ]; then
            poweroff
        fi
        exit 1
    else
        echo -e "\nFailed retrying...\n"
        if [ "$USBETHERNET" = "true" ]; then
            echo '1-1' > /sys/bus/usb/drivers/usb/unbind
            sleep 5
            echo '1-1' > /sys/bus/usb/drivers/usb/bind
        else
            ifconfig $INTERFACE down
            sleep 5
            ifconfig $INTERFACE up
        fi
    fi
done
