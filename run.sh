#!/bin/sh

if ! pgrep pppwn > /dev/null; then

    if [ -f /root/pw.conf ]; then

        source /root/pw.conf

        if /etc/init.d/pppoe-server status | grep -q "running"; then
            /etc/init.d/pppoe-server stop
            sleep 3
        fi
        
        ip link set $interface down
        sleep 5
        ip link set $interface up
        result=$(pppwn --interface "$interface" --fw "$version" --stage1 "$stage1" --stage2 "$stage2" --timeout $timeout --auto-retry)
        if [[ "$result" == *"\[\+\] Done\!"* ]]; then
            if /etc/init.d/pppoe-server status | grep -q "inactive"; then
                /etc/init.d/pppoe-server start
            fi
            echo "{\"output\":\"Exploit success\",\"pppwned\":true}"
            exit 0
        else
            if /etc/init.d/pppoe-server status | grep -q "inactive"; then
                /etc/init.d/pppoe-server start
            fi

            echo "{"
            echo "\"root\":\"$root\","
            echo "\"adapter\":\"$interface\","
            echo "\"version\":\"$version\","
            echo "\"timeout\":\"$timeout\""
            echo "}"

            exit 1
        fi

    fi

else
    
    pids=$(pgrep pppwn)
    for pid in $pids; do
        kill $pid
    done

    echo "{"
    echo "\"root\":\"$root\","
    echo "\"adapter\":\"$interface\","
    echo "\"version\":\"$version\","
    echo "\"timeout\":\"$timeout\""
    echo "}"

    exit 0
fi
