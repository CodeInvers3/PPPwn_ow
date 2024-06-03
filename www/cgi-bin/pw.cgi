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
option=$(echo $postData | sed -n 's/^.*option=\([^&]*\).*$/\1/p' | sed "s/%20/ /g")
root=$(echo $postData | sed -n 's/^.*root=\([^&]*\).*$/\1/p' | sed "s/%20/ /g")
root=$(echo "$root" | sed 's/%2F/\//g')

if [ -z "$timeout" ]; then
    timeout=0
fi
if [ -z "$root" ]; then
    root="/root"
fi

if [ "$token" = "token_id" ]; then

    case "$task" in
    "setup")

        source=""
        if [ "$option" = "aarch64-linux-musl" ]; then
            source="https://nightly.link/xfangfang/PPPwn_cpp/workflows/ci.yaml/main/aarch64-linux-musl.zip"
        elif [ "$option" = "arm-linux-musleabi(cortex_a7)" ]; then
            source="https://nightly.link/xfangfang/PPPwn_cpp/workflows/ci.yaml/main/arm-linux-musleabi%28cortex_a7%29.zip"
        elif [ "$option" = "arm-linux-musleabi(pi_zero_w)" ]; then
            source="https://nightly.link/xfangfang/PPPwn_cpp/workflows/ci.yaml/main/arm-linux-musleabi%28pi_zero_w%29.zip"
        elif [ "$option" = "arm-linux-musleabi(mpcorenovfp)" ]; then
            source="https://nightly.link/xfangfang/PPPwn_cpp/workflows/ci.yaml/main/arm-linux-musleabi%28mpcorenovfp%29.zip"
        elif [ "$option" = "x86_64-linux-musl" ]; then
            source="https://nightly.link/xfangfang/PPPwn_cpp/workflows/ci.yaml/main/x86_64-linux-musl.zip"
        elif [ "$option" = "mipsel-linux-musl" ]; then
            source="https://nightly.link/xfangfang/PPPwn_cpp/workflows/ci.yaml/main/mipsel-linux-musl.zip"
        elif [ "$option" = "mips-linux-musl" ]; then
            source="https://nightly.link/xfangfang/PPPwn_cpp/workflows/ci.yaml/main/mips-linux-musl.zip"
        fi

        cd /root/
        if ! command -v "unzip" > /dev/null 2>&1; then
            "$(opkg update)"
            "$(opkg install unzip)"
        fi
        if wget -O pppwn_file.zip "$source"; then
            "$(unzip pppwn_file.zip)"
            "$(rm pppwn_file.zip)"
            "$(tar -xzvf pppwn.tar.gz)"
            "$(rm pppwn.tar.gz)"
            "$(chmod +x pppwn)"
            "$(mv pppwn /usr/bin)"
            echo "{\"output\":\"PPPwn installed!\",\"pppwn\":true}"
        else
            echo "{\"output\":\"Cannot to get source: $source\"}"
        fi

    ;;
    "state")

        echo "{"
        if command -v pppwn > /dev/null 2>&1; then
            echo "\"pppwn\":true,"
            echo "\"interfaces\":["
            parts=$(pppwn list | sed "s/\s*$/\"},/")
            if [ "$parts" != "" ]; then
                eths=$(echo "$parts" | sed "s/^\s*/{\"adapter\":\"/")
                echo $eths | sed "s/,$//"
            fi
            echo "],";
            if pgrep pppwn > /dev/null; then
                echo "\"running\":true,"
            else
                echo "\"running\":false,"
                if [ -f "$signalfile" ]; then
                    rm $signalfile
                fi
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
        else
            echo "\"pppwn\":false,"
            echo "\"compiles\":["
            type=$(uname -m)
            if [ "$type" = "aarch64" ]; then
                echo "{\"label\":\"Arch64 Linux\",\"type\":\"aarch64-linux-musl\"}"
            elif [ "$type" = "arm" ]; then
                echo "{\"label\":\"Arm Cortex A7\",\"type\":\"arm-linux-musleabi(cortex_a7)\"},"
                echo "{\"label\":\"Arm Pi Zero W\",\"type\":\"arm-linux-musleabi(pi_zero_w)\"},"
                echo "{\"label\":\"Arm MP Core Nov Fp\",\"type\":\"arm-linux-musleabi(mpcorenovfp)\"}"
            elif [ "$type" = "x86_64" ]; then
                echo "{\"label\":\"X86-64 Linux\",\"type\":\"x86_64-linux-musl\"}"
            elif [ "$type" = "mips" ]; then
                echo "{\"label\":\"MIPSEL Linux\",\"type\":\"mipsel-linux-musl\"},"
                echo "{\"label\":\"MIPS Linux\",\"type\":\"mips-linux-musl\"}"
            elif [ "$type" = "mipsel" ]; then
                echo "{\"label\":\"MIPSEL Linux\",\"type\":\"mipsel-linux-musl\"}"
            fi
            echo "],"
        fi
        if grep -q "/root/run.sh" /etc/rc.local; then
            echo "\"autorun\":true"
        else
            echo "\"autorun\":false"
        fi
        echo "}"

    ;;
    "start")

        ip link set $adapter down
        sleep 5
        ip link set $adapter up

        if [ -f "$signalfile" ]; then
            rm $signalfile
        fi

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

            result=$(pppwn --interface "$adapter" --fw "$firmware" --stage1 $root/offsets/stage1_$firmware.bin --stage2 $root/offsets/stage2_$firmware.bin --timeout $timeout --auto-retry)
            echo "$result" > "/www/pppwn/register"
            
            if [ $? -eq 0 ]; then
                echo "{\"output\":\"Exploit success!\",\"pppwned\":true,\"attempts\":\"$attempts\"}"
                exit 0
            else
                attempts=$((attempts+1))
                ip link set $adapter down
                sleep 5
                ip link set $adapter up
            fi
        done

    ;;
    "stop")

        echo "stop" > $signalfile
        echo "{\"output\":\"Execution terminated.\",\"pppwned\":false,\"attempts\":\"$attempts\"}"

        pids=$(pgrep pppwn)
        for pid in $pids; do
            kill $pid
        done

        exit 1

    ;;
    "enable")

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
        chmod +x /root/run.sh
        echo "{\"output\":\"Autorun enable\"}"

    ;;
    "disable")

        if grep -q "/root/run.sh" /etc/rc.local; then
            sed -i '/\/root\/run\.sh/d' /etc/rc.local
        fi

        echo "{\"output\":\"Autorun disabled\"}"

    ;;
    "update")

        /root/update.sh
        
        exit 0
    ;;
    *)
        echo "{\"output\":\"null\"}"
        exit 1
    ;;
    esac

else
    echo "{\"output\":\"Invalid token!\"}"
    exit 1
fi