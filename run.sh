#!/bin/sh

if ! pgrep pppwn > /dev/null; then

    if [ -f /root/pw.conf ];then

        source /root/pw.conf

        if /etc/init.d/pppoe-server status | grep -q "running"; then
            /etc/init.d/pppoe-server stop
            sleep 3
        fi

        ip link set $interface down
        sleep 5
        ip link set $interface up
        
        res=$(pppwn --interface "$interface" --fw "$version" --stage1 "$stage1" --stage2 "$stage2" --timeout $timeout --auto-retry)
        
        if [ $res -eq 0 ]; then
            if /etc/init.d/pppoe-server status | grep -q "inactive"; then
                /etc/init.d/pppoe-server start
            fi
            exit 0
        else
            if /etc/init.d/pppoe-server status | grep -q "inactive"; then
                /etc/init.d/pppoe-server start
            fi
            exit 1
        fi

    fi

fi
