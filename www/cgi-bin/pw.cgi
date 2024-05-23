#!/bin/sh
echo "Content-Type: application/json"
echo ""

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
    
        echo "["
        parts=$(pppwn list | sed "s/\s*$/\",/")
        eths=$(echo "$parts" | sed "s/^\s*/\"/")
        echo $eths | sed "s/,$//"
        echo "]";

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
            pw=$(pppwn --interface "$adapter" --fw "$firmware" --stage1 "$root/offsets/stage1_$firmware.bin" --stage2 "$root/offsets/stage2_$firmware.bin" --auto-retry)
            if [ "$pw" -ge 1 ]; then
                echo "Exploit success!" > "/www/pppwn/state.txt"
                echo -e "{\"output\":\"Exploit success!\"}"
                exit 1
            elif [ -f $signalfile ]; then
                pids=$(pgrep pppwn)
                for pid in $pids; do
                    kill $pid
                done
                echo "Exploit pppwn stopped!" > "/www/pppwn/state.txt"
                echo -e "{\"output\":\"PPPwn stopped!\"}"
                exit 0
            else
                echo "Attempts ($countattempts)" > "/www/pppwn/state.txt"
                ip link set $adapter down
                sleep 5
                ip link set $adapter up
                echo -e "{\"output\":\"Attempts ($countattempts)\"}"
            fi
        done

    elif [ "$task" = "stop" ]; then

        echo "1" > $signalfile
        echo "{\"output\":\"Waiting response...\"}"

    elif [ "$task" = "enable" ]; then

        if ! grep -q "$root/run.sh" /etc/rc.local; then
            sed -i '/exit 0/d' /etc/rc.local
            echo "$root/run.sh &" >> /etc/rc.local
            echo 'exit 0' >> /etc/rc.local
        fi
        
        if grep -q "INTERFACE=" "$root/run.sh"; then
            sed -i "s/INTERFACE=\".*\"/INTERFACE=\"$adapter\"/" "$root/run.sh"
        fi
        if grep -q "FIRMWARE=" "$root/run.sh"; then
            sed -i "s/FIRMWARE=\".*\"/FIRMWARE=\"$firmware\"/" "$root/run.sh"
        fi

        echo "{\"output\":\"Autorun enable!\"}"

    elif [ "$task" = "disable" ]; then

        if grep -q "$root/run.sh" "$root/run.sh"; then
            sed -i "/$root/run.sh/d" "$root/run.sh"
        fi

        echo "{\"output\":\"Autorun disabled!\"}"

    fi

else

    echo "Invalid token!"
    exit 0

fi