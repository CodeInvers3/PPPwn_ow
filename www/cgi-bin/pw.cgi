#!/bin/sh
echo "Content-Type: application/json"
echo ""

token="token_id"
signalfile="/www/pppwn/stop"
attempts=0

read postData

token=$(echo $postData | sed -n 's/^.*token=\([^&]*\).*$/\1/p' | sed "s/%20/ /g")
adapter=$(echo $postData | sed -n 's/^.*adapter=\([^&]*\).*$/\1/p' | sed "s/%20/ /g")
firmware=$(echo $postData | sed -n 's/^.*firmware=\([^&]*\).*$/\1/p' | sed "s/%20/ /g")
timeout$(echo $postData | sed -n 's/^.*timeout=\([^&]*\).*$/\1/p' | sed "s/%20/ /g")
task=$(echo $postData | sed -n 's/^.*task=\([^&]*\).*$/\1/p' | sed "s/%20/ /g")
root=$(echo $postData | sed -n 's/^.*root=\([^&]*\).*$/\1/p' | sed "s/%20/ /g")
root=$(echo "$root" | sed 's/%2F/\//g')


if [ -z "$timeout" ]; then
    timeout=0
fi
if [ -z "$root" ]; then
    root="/root"
fi

if [ "$token" = "token_id" ]; then

    if [ "$task" = "state" ]; then
        
        pids=$(pgrep pppwn)
        echo "$pids"

    elif [ "$task" = "initialize" ]; then
        echo "{"

        if pgrep pppwn > /dev/null; then
            echo "\"running\":true,"
        else
            echo "\"running\":false,"
            if [ -f "$signalfile" ]; then
                rm $signalfile
            fi
        fi

        if grep -q "/root/run.sh" /etc/rc.local; then
            echo "\"active\":true,"
        else
            echo "\"active\":false,"
        fi

        payloads=$(ls /root/offsets/*.bin)
        count=0
        filename=""
        separator=""
        echo "\"offsets\":["
        for payload in $payloads; do
            if echo "$payload" | grep -q "stage1"; then
                stage="$payload"
            fi
            if echo "$payload" | grep -q "stage2"; then
                if [ "$count" -gt "0" ]; then
                    separator=","
                fi
                filename=$(echo $payload | sed -e 's/.*_//g' -e 's/\.bin//g')
                echo "$separator{\"version\":\"$filename\",\"stage_2\":\"$payload\",\"stage_1\":\"$stage\"}"
                count=$((count+1))
            fi
        done
        echo "],"

        echo "\"interfaces\":["
        parts=$(pppwn list | sed "s/\s*$/\"},/")
        eths=$(echo "$parts" | sed "s/^\s*/{\"adapter\":\"/")
        echo $eths | sed "s/,$//"
        echo "]}";

    elif [ "$task" = "run" ]; then
        
        ip link set $adapter down
        sleep 5
        ip link set $adapter up

        while true; do

            if [ -f "$signalfile" ]; then
            
                echo "{\"output\":\"Waiting response...\"}"

                pids=$(pgrep pppwn)
                for pid in $pids; do
                    kill $pid
                done

                if [ -f "$signalfile" ]; then
                    rm $signalfile
                fi
                
                exit 1
            fi

            pppwn --interface "$adapter" --fw "$firmware" --stage1 $root/offsets/stage1_$firmware.bin --stage2 $root/offsets/stage2_$firmware.bin --timeout $timeout --auto-retry
            
            if [ $? -eq 0 ]; then
                echo "{\"output\":\"Exploit success!\",\"pppwn\":true,\"attempts\":\"$attempts\"}" > "/www/pppwn/state.json"
                exit 0
            else
                attempts=$((attempts+1))
                ip link set $adapter down
                sleep 5
                ip link set $adapter up
            fi
        done

    elif [ "$task" = "stop" ]; then

        echo "stop" > $signalfile
        echo "{\"output\":\"Execution terminated.\",\"pppwn\":false,\"attempts\":\"$attempts\"}"

        pids=$(pgrep pppwn)
        for pid in $pids; do
            kill $pid
        done

        exit 1

    elif [ "$task" = "enable" ]; then

        if ! grep -q "/root/run.sh" /etc/rc.local; then
            sed -i '/exit 0/d' /etc/rc.local
            echo "/root/run.sh &" >> /etc/rc.local
            echo "exit 0" >> /etc/rc.local
        fi
        
        if grep -q "interface=" "/root/run.sh"; then
            sed -i "s/interface=\".*\"/interface=\"$adapter\"/" "/root/run.sh"
        fi
        if grep -q "firmware=" "/root/run.sh"; then
            sed -i "s/firmware=\".*\"/firmware=\"$firmware\"/" "/root/run.sh"
        fi

        chmod +x /etc/rc.local
        echo "{\"output\":\"Autorun enable\"}"

    elif [ "$task" = "disable" ]; then

        if grep -q "/root/run.sh" /etc/rc.local; then
            sed -i '/\/root\/run\.sh/d' /etc/rc.local
        fi

        echo "{\"output\":\"Autorun disabled\"}"

    fi

else
    echo "{\"output\":\"Invalid token!\"}"
    exit 1
fi