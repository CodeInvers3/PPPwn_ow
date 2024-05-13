#!/bin/sh /etc/rc.common

if ! grep -q '/root/run.sh' /etc/rc.local; then
    sed -i '/exit 0/d' /etc/rc.local
    echo '/root/run.sh &' >> /etc/rc.local
    echo 'exit 0' >> /etc/rc.local
fi
reboot
