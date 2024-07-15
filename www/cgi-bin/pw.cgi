#!/bin/sh

echo "Content-Type: application/json"

token="token_id"
stoken=""
token_file="/tmp/token"

if ! [ -f "$token_file" ]; then
    stoken=$(head -30 /dev/urandom | tr -dc "0123456789" | head -c20)
    echo "$stoken" > "$token_file"
else
    stoken=$(cat "$token_file")
fi

read postData

token=$(echo $postData | sed -n 's/^.*token=\([^&]*\).*$/\1/p' | sed "s/%20/ /g")
adapter=$(echo $postData | sed -n 's/^.*adapter=\([^&]*\).*$/\1/p' | sed "s/%20/ /g")
version=$(echo $postData | sed -n 's/^.*version=\([^&]*\).*$/\1/p' | sed "s/%20/ /g")
stage1=$(echo $postData | sed -n 's/^.*stage1=\([^&]*\).*$/\1/p' | sed "s/%20/ /g")
stage1=$(echo "$stage1" | sed 's/%2F/\//g')
stage2=$(echo $postData | sed -n 's/^.*stage2=\([^&]*\).*$/\1/p' | sed "s/%20/ /g")
stage2=$(echo "$stage2" | sed 's/%2F/\//g')
timeout=$(echo $postData | sed -n 's/^.*timeout=\([^&]*\).*$/\1/p' | sed "s/%20/ /g")
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

case "$task" in
    "setup")

        if ! [ "$token" = "$stoken" ]; then

            echo "Status: 400 Bad Request"
            echo ""
            echo "{\"output\":\"Invalid token\"}"
            exit 1
            
        fi

        echo ""

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
        elif [ "$option" = "custom-aarch64-linux-musl" ]; then
            source="https://raw.githubusercontent.com/CodeInvers3/pppwn_custom/main/compiled/aarch64-linux-musl/pppwn"
        elif [ "$option" = "custom-arm-linux-musleabi_cortex_a7" ]; then
            source="https://raw.githubusercontent.com/CodeInvers3/pppwn_custom/main/compiled/arm-linux-musleabi_cortex_a7/pppwn"
        elif [ "$option" = "custom-arm-linux-musleabi_mpcorenovfp" ]; then
            source="https://raw.githubusercontent.com/CodeInvers3/pppwn_custom/main/compiled/arm-linux-musleabi_mpcorenovfp/pppwn"
        elif [ "$option" = "custom-arm-linux-musleabi_pi_zero_w" ]; then
            source="https://raw.githubusercontent.com/CodeInvers3/pppwn_custom/main/compiled/arm-linux-musleabi_pi_zero_w/pppwn"
        elif [ "$option" = "custom-mips-linux-musl" ]; then
            source="https://raw.githubusercontent.com/CodeInvers3/pppwn_custom/main/compiled/mips-linux-musl/pppwn"
        elif [ "$option" = "custom-mipsel-linux-musl" ]; then
            source="https://raw.githubusercontent.com/CodeInvers3/pppwn_custom/main/compiled/mipsel-linux-musl/pppwn"
        elif [ "$option" = "custom-x86_64-linux-musl" ]; then
            source="https://raw.githubusercontent.com/CodeInvers3/pppwn_custom/main/compiled/x86_64-linux-musl/pppwn"
        fi

        if [[ "$source" =~ \.zip$ ]]; then
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
                echo "{\"output\":\"PPPwn installed\",\"pppwn\":true}"
                exit 0
            else
                echo "{\"output\":\"Cannot to get source: $source\"}"
                exit 1
            fi
        else
            "$(wget -O /usr/bin/pppwn $source)"
            "$(chmod +x /usr/bin/pppwn)"
            echo "{\"output\":\"PPPwn installed\",\"pppwn\":true}"
            exit 0
        fi

    ;;
    "state")

        echo ""
        echo "{"

        current_version=$(cat /root/version)
        latest_version=$(wget -qO- "https://raw.githubusercontent.com/CodeInvers3/PPPwn_ow/main/version" 2>/dev/null)

        echo "\"stored_token\":\"$stoken\","
        echo "\"chipname\":\"$(uname -m)\","

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
                echo "\"version\":\"$version\","
                echo "\"timeout\":\"$timeout\","
            fi
        else
            echo "\"pppwn\":false,"
            echo "\"compiled\":["
            type=$(uname -m)
            if echo "$type" | grep -q "aarch64"; then
                echo "{\"label\":\"Arch64 Linux\",\"type\":\"aarch64-linux-musl\"},"
                echo "{\"label\":\"Custom Arch64 Linux\",\"type\":\"custom-aarch64-linux-musl\"}"
            elif echo "$type" | grep -q "arm"; then
                echo "{\"label\":\"ARM Cortex A7\",\"type\":\"arm-linux-musleabi(cortex_a7)\"},"
                echo "{\"label\":\"ARM Pi Zero W\",\"type\":\"arm-linux-musleabi(pi_zero_w)\"},"
                echo "{\"label\":\"ARM MP Core Nov Fp\",\"type\":\"arm-linux-musleabi(mpcorenovfp)\"},"
                echo "{\"label\":\"Custom ARM Cortex A7\",\"type\":\"custom-arm-linux-musleabi_cortex_a7\"},"
                echo "{\"label\":\"Custom ARM MP Core Nov\",\"type\":\"custom-arm-linux-musleabi_mpcorenovfp\"},"
                echo "{\"label\":\"Custom ARM Pi Zero W\",\"type\":\"custom-arm-linux-musleabi_pi_zero_w\"}"
            elif echo "$type" | grep -q "x86_64"; then
                echo "{\"label\":\"X86-64 Linux\",\"type\":\"x86_64-linux-musl\"},"
                echo "{\"label\":\"Custom x86_64 Linux\",\"type\":\"custom-x86_64-linux-musl\"}"
            elif echo "$type" | grep -q "mips"; then
                echo "{\"label\":\"MIPSEL Linux\",\"type\":\"mipsel-linux-musl\"},"
                echo "{\"label\":\"MIPS Linux\",\"type\":\"mips-linux-musl\"},"
                echo "{\"label\":\"Custom MIPSEL Linux\",\"type\":\"custom-mipsel-linux-musl\"},"
                echo "{\"label\":\"Custom MIPS\",\"type\":\"custom-mips-linux-musl\"}"
            elif "$type" | grep -q "mipsel"; then
                echo "{\"label\":\"MIPSEL Linux\",\"type\":\"mipsel-linux-musl\"},"
                echo "{\"label\":\"Custom MIPSEL Linux\",\"type\":\"custom-mipsel-linux-musl\"}"
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

        if ! [ "$token" = "$stoken" ]; then

            echo "Status: 400 Bad Request"
            echo ""
            echo "{\"output\":\"Invalid token\"}"
            exit 1
            
        fi

        echo ""
        if [ -f /root/pw.conf ]; then
            sed -i "s/interface=.*/interface=$adapter/" "/root/pw.conf"
            sed -i "s/version=.*/version=$version/" "/root/pw.conf"
            sed -i "s/timeout=.*/timeout=$timeout/" "/root/pw.conf"
        else
            echo -e "interface=$adapter\n" > "/root/pw.conf"
            echo -e "version=$version\n" >> "/root/pw.conf"
            echo -e "timeout=$timeout\n" >> "/root/pw.conf"
        fi
        /root/run.sh

    ;;
    "stop")

        if ! [ "$token" = "$stoken" ]; then

            echo "Status: 400 Bad Request"
            echo ""
            echo "{\"output\":\"Invalid token\"}"
            exit 1
            
        fi

        echo ""
        pids=$(pgrep pppwn)
        for pid in $pids; do
            kill $pid
        done

        echo "{\"output\":\"Execution terminated.\",\"pppwned\":false}"

        exit 1

    ;;
    "params")

        if ! [ "$token" = "$stoken" ]; then

            echo "Status: 400 Bad Request"
            echo ""
            echo "{\"output\":\"Invalid token\"}"
            exit 1
            
        fi

        echo ""
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

        echo "{\"output\":\"Settings saved\"}"

    ;;
    "enable")

        if ! [ "$token" = "$stoken" ]; then

            echo "Status: 400 Bad Request"
            echo ""
            echo "{\"output\":\"Invalid token\"}"
            exit 1
            
        fi

        echo ""
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
        echo "{\"output\":\"Autorun enabled\"}"

    ;;
    "disable")

        if ! [ "$token" = "$stoken" ]; then

            echo "Status: 400 Bad Request"
            echo ""
            echo "{\"output\":\"Invalid token\"}"
            exit 1
            
        fi

        echo ""
        if grep -q "/root/run.sh" /etc/rc.local; then
            sed -i '/\/root\/run\.sh/d' /etc/rc.local
        fi
        echo "{\"output\":\"Autorun disabled\"}"

    ;;
    "update")

        if ! [ "$token" = "$stoken" ]; then

            echo "Status: 400 Bad Request"
            echo ""
            echo "{\"output\":\"Invalid token\"}"
            exit 1
            
        fi

        echo ""
        "$(wget -O /tmp/installer.sh https://raw.githubusercontent.com/CodeInvers3/PPPwn_ow/main/installer.sh)"
        chmod +x /tmp/installer.sh
        if command -v pppwn > /dev/null 2>&1; then
            rm /usr/bin/pppwn
        fi
        "$(/tmp/installer.sh)"
        if [ -f /tmp/installer.sh ]; then
            rm -r /tmp/installer.sh
        fi
        echo "{\"output\":\"Update completed\"}"
        
    ;;
    "remove")

        if ! [ "$token" = "$stoken" ]; then
             echo "Status: 400 Bad Request"
             echo ""
             echo "{\"output\":\"Invalid token\"}"
             exit 1
        fi

        echo ""
        rm -f /usr/bin/pppwn
        rm -rf /root/*
        rm -rf /www/pppwn
        rm -f /www/pppwn.html
        rm -f /www/cgi-bin/pw.cgi
        echo "{\"output\":\"Uninstalled\"}"
        
    ;;
    "connect")

        if ! [ "$token" = "$stoken" ]; then

            echo "Status: 400 Bad Request"
            echo ""
            echo "{\"output\":\"Invalid token\"}"
            exit 1
            
        fi

        echo ""
        echo "{"
        if /etc/init.d/pppoe-server status | grep -q "running"; then
            /etc/init.d/pppoe-server stop
            echo "\"output\":\"PPPoE service stopped\","
        elif /etc/init.d/pppoe-server status | grep -q "inactive"; then
            /etc/init.d/pppoe-server start
            echo "\"output\":\"PPPoE service started\","
        fi
        rspppoe=$(/etc/init.d/pppoe-server status)
        echo "\"pppoe\":\"$rspppoe\""
        echo "}"

    ;;
    "add_func")

        if ! [ "$token" = "$stoken" ]; then

            echo "Status: 400 Bad Request"
            echo ""
            echo "{\"output\":\"Invalid token\"}"
            exit 1
            
        fi

        echo ""
        if ! grep -q "/root/run.sh" /etc/rc.button/switch; then
            sed -i "s/action=on/action=on\n\n\/root\/run\.sh/" /etc/rc.button/switch
        fi

    ;;
    *)

        echo "Status: 400 Bad Request"
        echo ""
        echo "{\"output\":\"Invalid task\"}"
        exit 1

    ;;
esac