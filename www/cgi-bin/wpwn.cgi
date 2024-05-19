#!/bin/sh
echo "Content-Type: application/json"
echo ""

adapter="br-lan"
firmware="1100"
token="token_id"
countattempts=0
signalfile="/www/pppwn/stop"

read postData

token=$(echo $postData | sed -n 's/^.*token=\([^&]*\).*$/\1/p' | sed "s/%20/ /g")
adapter=$(echo $postData | sed -n 's/^.*adapter=\([^&]*\).*$/\1/p' | sed "s/%20/ /g")
firmware=$(echo $postData | sed -n 's/^.*firmware=\([^&]*\).*$/\1/p' | sed "s/%20/ /g")
eroot=$(echo $postData | sed -n 's/^.*root=\([^&]*\).*$/\1/p' | sed "s/%20/ /g")
task=$(echo $postData | sed -n 's/^.*task=\([^&]*\).*$/\1/p' | sed "s/%20/ /g")
root=$(echo "$eroot" | sed 's/%2F/\//g')

if [ "$token" = "token_id" ]; then

    if [ "$task" = "adapters" ]; then

        eths=$(~/pppwn list)
        echo "$eths"

    elif [ "$task" = "payloads" ]; then

        payloads=$(ls ~/offsets/*.bin)
        count=0
        separator=""
        echo "["

        for payload in $payloads; do
            if echo "$payload" | grep -q "stage1"; then
                if [ "$count" -gt "0" ]; then
                    separator=","
                fi
                prts=$(echo $payload | sed -e 's/.*_/ /g' -e 's/\.bin/ /g')
                echo "$separator\"$prts\""
            fi
            count=$((count+1))
        done
        echo "]"

    elif [ "$task" = "run" ]; then
    
        if [ -f "$signalfile" ]; then
            rm "$signalfile"
        fi
        
        ip link set $adapter down
        sleep 5
        ip link set $adapter up
        
        while true; do

            countattempts=$((countattempts+1))
            pwn=$($root/pppwn --interface "$adapter" --fw $firmware --stage1 $root/offsets/stage1_$firmware.bin --stage2 $root/offsets/stage2_$firmware.bin --auto-retry)
            if [ "$pwn" -ge 1 ]; then
                echo "Exploit success!" > "/www/pppwn/state.txt"
                exit 0
            else
                echo "Failed! attempting($countattempts)..." > "/www/pppwn/state.txt"
                ip link set $adapter down
                sleep 5
                ip link set $adapter up
            fi
            if [ -f "$signalfile" ]; then
                pids=$(pgrep ~/pppwn)
                for pid in $pids; do
                    kill $pid
                done
                echo "Termination signal detected. Exiting loop." > "/www/pppwn/state.txt"
                exit 0
            fi

        done

    elif [ "$task" = "stop" ]; then

        pids=$(pgrep pppwn)
        for pid in $pids; do
            kill $pid
        done

        echo "stop=true" > "$signalfile"

    elif [ "$task" = "enable" ]; then

        if ! grep -q "$root/run.sh" /etc/rc.local; then
            sed -i '/exit 0/d' /etc/rc.local
            echo "$root/run.sh &" >> /etc/rc.local
            echo 'exit 0' >> /etc/rc.local
        fi
        echo "Enabled!"

    fi

else

    echo "Invalid token!"

fi