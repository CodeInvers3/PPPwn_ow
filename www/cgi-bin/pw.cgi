#!/bin/sh

echo "Content-Type: application/json"
echo ""

token="token_id"
attempts=0

read postData

token=$(echo $postData | sed -n 's/^.*token=\([^&]*\).*$/\1/p' | sed "s/%20/ /g")
adapter=$(echo $postData | sed -n 's/^.*adapter=\([^&]*\).*$/\1/p' | sed "s/%20/ /g")
version=$(echo $postData | sed -n 's/^.*version=\([^&]*\).*$/\1/p' | sed "s/%20/ /g")
stage1=$(echo $postData | sed -n 's/^.*stage1=\([^&]*\).*$/\1/p' | sed "s/%20/ /g")
stage1=$(echo "$stage1" | sed 's/%2F/\//g')
stage2=$(echo $postData | sed -n 's/^.*stage2=\([^&]*\).*$/\1/p' | sed "s/%20/ /g")
stage2=$(echo "$stage2" | sed 's/%2F/\//g')
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

        if ! command -v "unzip" > /dev/null 2>&1; then
            "$(opkg update)"
            "$(opkg install unzip)"
        fi

        cd /tmp/
        if wget -O pppwn_file.zip $source; then
            "$(unzip pppwn_file.zip)"
            "$(rm pppwn_file.zip)"
            "$(tar -xzvf pppwn.tar.gz)"
            "$(rm pppwn.tar.gz)"
            "$(chmod +x pppwn)"
            "$(mv pppwn /usr/bin)"
            echo "{\"output\":\"PPPwn installed!\",\"pppwn\":true}"
            exit 0
        else
            echo "{\"output\":\"Cannot to get source: $source\"}"
            exit 1
        fi

    ;;
    "state")

        echo "{"

        current_version=$(cat /root/version)
        latest_version=$(wget -qO- "https://raw.githubusercontent.com/CodeInvers3/PPPwn_ow/main/version" 2>/dev/null)

        if [ -z "$latest_version" ]; then
            echo "\"update\":false,"
        else
            if [ "$current_version" != "$latest_version" ]; then
                echo "\"update\":true,"
            else
                echo "\"update\":false,"
            fi
        fi

        if command -v pppoe-server >/dev/null 2>&1; then
            rspppoe=$(/etc/init.d/pppoe-server status)
            echo "\"pppoe\":\"$rspppoe\","
        fi
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
            fi
            payloads1=$(ls /root/stage1/*.bin)
            payloads2=$(ls /root/stage2/*.bin)
            separator=""
            echo "\"versions\":["
            for payload in $payloads1; do

                filename=$(basename "$payload" | sed 's/\.bin$//')
                echo "$separator\"$filename\""
                if [ "$separator" = "" ]; then
                    separator=","
                fi

            done
            separator=""
            echo "],\"stage1\":{"
            for payload in $payloads1; do

                filename=$(basename "$payload" | sed 's/\.bin$//')
                echo "$separator\"$filename\":\"$payload\""

                if [ "$separator" = "" ]; then
                    separator=","
                fi

            done
            separator=""
            echo "},\"stage2\":{"
            for payload in $payloads2; do

                filename=$(basename "$payload" | sed 's/\.bin$//')
                echo "$separator\"$filename\":\"$payload\""

                if [ "$separator" = "" ]; then
                    separator=","
                fi

            done
            echo "},"
            if [ -f /root/pw.conf ];then
                source /root/pw.conf
                echo "\"adapter\":\"$interface\","
                echo "\"timeout\":\"$timeout\","
                echo "\"version\":\"$version\","
            fi
        else
            echo "\"pppwn\":false,"
            echo "\"compiles\":["
            type=$(uname -m)
            if echo "$type" | grep -q "arch64"; then
                echo "{\"label\":\"Arch64 Linux\",\"type\":\"aarch64-linux-musl\"}"
            elif echo "$type" | grep -q "arm"; then
                echo "{\"label\":\"Arm Cortex A7\",\"type\":\"arm-linux-musleabi(cortex_a7)\"},"
                echo "{\"label\":\"Arm Pi Zero W\",\"type\":\"arm-linux-musleabi(pi_zero_w)\"},"
                echo "{\"label\":\"Arm MP Core Nov Fp\",\"type\":\"arm-linux-musleabi(mpcorenovfp)\"}"
            elif echo "$type" | grep -q "x86_64"; then
                echo "{\"label\":\"X86-64 Linux\",\"type\":\"x86_64-linux-musl\"}"
            elif echo "$type" | grep -q "mips"; then
                echo "{\"label\":\"MIPSEL Linux\",\"type\":\"mipsel-linux-musl\"},"
                echo "{\"label\":\"MIPS Linux\",\"type\":\"mips-linux-musl\"}"
            elif "$type" | grep -q "mipsel"; then
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

        if [ -f /root/pw.conf ]; then
            sed -i "s/interface=.*/interface=$adapter/" /root/pw.conf
            sed -i "s/timeout=.*/timeout=$timeout/" /root/pw.conf
            sed -i "s/version=.*/version=$version/" /root/pw.conf
        else
            echo -e "interface=$adapter\n" > /root/pw.conf
            echo -e "timeout=$timeout\n" >> /root/pw.conf
            echo -e "version=$version\n" >> /root/pw.conf
        fi

        if /etc/init.d/pppoe-server status | grep -q "running"; then
            /etc/init.d/pppoe-server stop
            sleep 3
        fi

        ip link set $adapter down
        sleep 5
        ip link set $adapter up

        attempts=$((attempts+1))

        result=$(pppwn --interface "$adapter" --fw "$version" --stage1 "$stage1" --stage2 "$stage2" --timeout $timeout --auto-retry)
        
        if [[ "$result" == *"\[\+\] Done\!"* ]]; then
            /etc/init.d/pppoe-server start
            echo "{\"output\":\"Exploit success!\",\"pppwned\":true,\"attempts\":\"$attempts\"}"
            exit 0
        else
            echo "{\"output\":\"Exploit interrupted!\",\"pppwned\":false,\"attempts\":\"$attempts\"}"
            exit 1
        fi

    ;;
    "stop")

        pids=$(pgrep pppwn)
        for pid in $pids; do
            kill $pid
        done

        echo "{\"output\":\"Execution terminated.\",\"pppwned\":false,\"attempts\":\"$attempts\"}"

        exit 1

    ;;
    "enable")

        if ! grep -q "/root/run.sh" /etc/rc.local; then
            sed -i '/exit 0/d' /etc/rc.local
            echo "/root/run.sh &" >> /etc/rc.local
            echo "exit 0" >> /etc/rc.local
        fi

        if [ -f /root/pw.conf ]; then

            if grep -q "interface=" "/root/pw.conf"; then
                sed -i "s/interface=.*/interface=$adapter/" "/root/pw.conf"
            else
                echo -e "interface=$adapter" >> "/root/pw.conf"
            fi
            if grep -q "version=" "/root/pw.conf"; then
                sed -i "s/version=.*/version=$version/" "/root/pw.conf"
            else
                echo -e "version=$version" >> "/root/pw.conf"
            fi
            if grep -q "timeout=" "/root/pw.conf"; then
                sed -i "s/timeout=.*/timeout=$timeout/" "/root/pw.conf"
            else
                echo -e "timeout=$timeout" >> "/root/pw.conf"
            fi
            if grep -q "stage1=" "/root/pw.conf"; then
                sed -i "/stage1=.*/d" "/root/pw.conf"
                echo -e "stage1=$stage1" >> "/root/pw.conf"
            fi
            if grep -q "stage2=" "/root/pw.conf"; then
                sed -i "/stage2=.*/d" "/root/pw.conf"
                echo -e "stage2=$stage2" >> "/root/pw.conf"
            fi
        else
            echo -e "interface=$adapter" > /root/pw.conf
            echo -e "version=$version" >> /root/pw.conf
            echo -e "timeout=$timeout" >> /root/pw.conf
            echo -e "stage1=$stage1" >> /root/pw.conf
            echo -e "stage2=$stage2" >> /root/pw.conf
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

        "$(cd /root/)"
        if [ -d /root/offsets ]; then
            "$(rm -r /root/offsets)"
        fi
        if [ -d /root/stage1 ]; then
            "$(rm -r /root/stage1)"
        fi
        if [ -d /root/stage2 ]; then
            "$(rm -r /root/stage2)"
        fi
        if [ -d /www/pppwn ]; then
            "$(rm -r /www/pppwn)"
        fi
        if [ -f /www/pppwn.html ]; then
            "$(rm /www/pppwn.html)"
        fi
        if [ -f /www/cgi-bin/pw.cgi ]; then
            "$(rm /www/cgi-bin/pw.cgi)"
        fi
        if [ -f /root/run.sh ]; then
            "$(rm /root/run.sh)"
        fi
        if command -v pppwn > /dev/null 2>&1; then
            "$(rm /usr/bin/pppwn)"
        fi
        if ! command -v unzip > /dev/null 2>&1; then
            "$(opkg update)"
            "$(opkg install unzip)"
        fi

        "$(cd /tmp/)"
        
        "$(wget -O main.zip https://github.com/CodeInvers3/PPPwn_ow/archive/refs/heads/main.zip)"
        "$(unzip main.zip)"
        
        cd PPPwn_ow-main
        
        "$(mv -f version /root/)"
        "$(mv -f stage1 /root/)"
        "$(mv -f stage2 /root/)"
        "$(mv -f run.sh /root/)"
        "$(mv -f www/pppwn /www)"
        "$(mv -f www/pppwn.html /www)"
        "$(mv -f www/cgi-bin/pw.cgi /www/cgi-bin)"
        
        cd ..
        
        "$(rm -r PPPwn_ow-main main.zip)"
        "$(chmod +x /www/cgi-bin/pw.cgi)"
        echo "{\"output\":\"Update completed!\"}"
        exit 0
        
    ;;
    "connect")

        echo "{"
        if /etc/init.d/pppoe-server status | grep -q "running"; then
            /etc/init.d/pppoe-server stop
            echo "\"output\":\"Stop pppoe service\","
        elif /etc/init.d/pppoe-server status | grep -q "inactive"; then
            /etc/init.d/pppoe-server start
            echo "\"output\":\"Start pppoe service\","
        fi
        rspppoe=$(/etc/init.d/pppoe-server status)
        echo "\"pppoe\":\"$rspppoe\""
        echo "}"

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