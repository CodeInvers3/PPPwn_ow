#!/bin/sh

if ! pgrep pppwn > /dev/null; then

    if [ -f /root/pw.conf ];then

        source /root/pw.conf
        
        ip link set $interface down
        sleep 5
        ip link set $interface up
        
        result=$(pppwn --interface "$interface" --fw "$version" --stage1 "$stage1" --stage2 "$stage2" --timeout $timeout --auto-retry)
        if [[ "$result" == *"\[\+\] Done\!"* ]]; then
            echo "PPPwn Success"
            exit 0
        else
            echo "PPPwn fail"
            exit 1
        fi

    fi

else
    echo "PPPwn is not installed"
    exit 1
fi
