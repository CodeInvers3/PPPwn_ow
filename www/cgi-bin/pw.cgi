#!/bin/sh

echo "Content-Type: application/json"

token="token_id"
stoken=""
token_file="/tmp/token"
rspppoe=$(pgrep pppoe-server)

if ! [ -f "$token_file" ]; then
    stoken=$(head -30 /dev/urandom | tr -dc "0123456789" | head -c20)
    echo "$stoken" > "$token_file"
else
    stoken=$(cat "$token_file")
fi

read postData

token=$(echo $postData | sed -n 's/^.*token=\([^&]*\).*$/\1/p' | sed "s/%20/ /g")
adapter=$(echo $postData | sed -n 's/^.*adapter=\([^&]*\).*$/\1/p' | sed "s/%20/ /g")
adapter=$(echo "$adapter" | sed 's/+/ /g')
version=$(echo $postData | sed -n 's/^.*version=\([^&]*\).*$/\1/p' | sed "s/%20/ /g")
stage1=$(echo $postData | sed -n 's/^.*stage1=\([^&]*\).*$/\1/p' | sed "s/%20/ /g")
stage1=$(echo "$stage1" | sed 's/%2F/\//g')
stage2=$(echo $postData | sed -n 's/^.*stage2=\([^&]*\).*$/\1/p' | sed "s/%20/ /g")
stage2=$(echo "$stage2" | sed 's/%2F/\//g')
timeout=$(echo $postData | sed -n 's/^.*timeout=\([^&]*\).*$/\1/p' | sed "s/%20/ /g")
auto=$(echo $postData | sed -n 's/^.*auto=\([^&]*\).*$/\1/p' | sed "s/%20/ /g")
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

set_params(){

    if [ -f /root/pw.conf ]; then
            
        if grep -q "root=" "/root/pw.conf"; then
            sed -i "s/root=.*/root=\"$root\"/" "/root/pw.conf"
        else
            echo -e "root=\"$root\"" >> "/root/pw.conf"
        fi
        if grep -q "interface=" "/root/pw.conf"; then
            sed -i "s/interface=.*/interface=\"$adapter\"/" "/root/pw.conf"
        else
            echo -e "interface=\"$adapter\"" >> "/root/pw.conf"
        fi
        if grep -q "version=" "/root/pw.conf"; then
            sed -i "s/version=.*/version=\"$version\"/" "/root/pw.conf"
        else
            echo -e "version=\"$version\"" >> "/root/pw.conf"
        fi
        if grep -q "timeout=" "/root/pw.conf"; then
            sed -i "s/timeout=.*/timeout=\"$timeout\"/" "/root/pw.conf"
        else
            echo -e "timeout=\"$timeout\"" >> "/root/pw.conf"
        fi
        if grep -q "stage1=" "/root/pw.conf"; then
            sed -i "/stage1=.*/d" "/root/pw.conf"
            echo -e "stage1=\"$stage1\"" >> "/root/pw.conf"
        fi
        if grep -q "stage2=" "/root/pw.conf"; then
            sed -i "/stage2=.*/d" "/root/pw.conf"
            echo -e "stage2=\"$stage2\"" >> "/root/pw.conf"
        fi
    else
        echo -e "root=\"$root\"" > /root/pw.conf
        echo -e "interface=\"$adapter\"" > /root/pw.conf
        echo -e "version=\"$version\"" >> /root/pw.conf
        echo -e "timeout=\"$timeout\"" >> /root/pw.conf
        echo -e "stage1=\"$stage1\"" >> /root/pw.conf
        echo -e "stage2=\"$stage2\"" >> /root/pw.conf
    fi

}

case "$task" in
    "setup")

        if ! [ "$token" = "$stoken" ]; then

            echo "Status: 400 Bad Request"
            echo ""
            echo "{\"output\":\"Invalid token\"}"
            exit 1
            
        fi

        echo ""

        repo_refs=""
        if [ "$option" = "aarch64-linux-musl" ]; then
            repo_refs="https://raw.githubusercontent.com/CodeInvers3/codeinvers3.github.io/master/custom/stored/aarch64-linux-musl.tar.gz"
        elif [ "$option" = "arm-linux-musleabi(cortex_a7)" ]; then
            repo_refs="https://raw.githubusercontent.com/CodeInvers3/codeinvers3.github.io/master/custom/stored/arm-linux-musleabi(cortex_a7).tar.gz"
        elif [ "$option" = "arm-linux-musleabi(pi_zero_w)" ]; then
            repo_refs="https://raw.githubusercontent.com/CodeInvers3/codeinvers3.github.io/master/custom/stored/arm-linux-musleabi(pi_zero_w).tar.gz"
        elif [ "$option" = "arm-linux-musleabi(mpcorenovfp)" ]; then
            repo_refs="https://raw.githubusercontent.com/CodeInvers3/codeinvers3.github.io/master/custom/stored/arm-linux-musleabi(mpcorenovfp).tar.gz"
        elif [ "$option" = "x86_64-linux-musl" ]; then
            repo_refs="https://raw.githubusercontent.com/CodeInvers3/codeinvers3.github.io/master/custom/stored/x86_64-linux-musl.tar.gz"
        elif [ "$option" = "mipsel-linux-musl" ]; then
            repo_refs="https://raw.githubusercontent.com/CodeInvers3/codeinvers3.github.io/master/custom/stored/mipsel-linux-musl.tar.gz"
        elif [ "$option" = "mips-linux-musl" ]; then
            repo_refs="https://raw.githubusercontent.com/CodeInvers3/codeinvers3.github.io/master/custom/stored/mips-linux-musl.tar.gz"
        elif [ "$option" = "custom-aarch64-linux-musl" ]; then
            repo_refs="https://raw.githubusercontent.com/CodeInvers3/codeinvers3.github.io/master/custom/compiled/aarch64-linux-musl/pppwn"
        elif [ "$option" = "custom-arm-linux-musleabi_cortex_a7" ]; then
            repo_refs="https://raw.githubusercontent.com/CodeInvers3/codeinvers3.github.io/master/custom/compiled/arm-linux-musleabi_cortex_a7/pppwn"
        elif [ "$option" = "custom-arm-linux-musleabi_mpcorenovfp" ]; then
            repo_refs="https://raw.githubusercontent.com/CodeInvers3/codeinvers3.github.io/master/custom/compiled/arm-linux-musleabi_mpcorenovfp/pppwn"
        elif [ "$option" = "custom-arm-linux-musleabi_pi_zero_w" ]; then
            repo_refs="https://raw.githubusercontent.com/CodeInvers3/codeinvers3.github.io/master/custom/compiled/arm-linux-musleabi_pi_zero_w/pppwn"
        elif [ "$option" = "custom-mips-linux-musl" ]; then
            repo_refs="https://raw.githubusercontent.com/CodeInvers3/codeinvers3.github.io/master/custom/compiled/mips-linux-musl/pppwn"
        elif [ "$option" = "custom-mipsel-linux-musl" ]; then
            repo_refs="https://raw.githubusercontent.com/CodeInvers3/codeinvers3.github.io/master/custom/compiled/mipsel-linux-musl/pppwn"
        elif [ "$option" = "custom-x86_64-linux-musl" ]; then
            repo_refs="https://raw.githubusercontent.com/CodeInvers3/codeinvers3.github.io/master/custom/compiled/x86_64-linux-musl/pppwn"
        fi

        if [[ "$repo_refs" =~ tar\.gz$ ]]; then
            cd /tmp/
            if wget -O pppwn.tar.gz $repo_refs; then
                "$(tar -xzvf pppwn.tar.gz)"
                "$(rm pppwn.tar.gz)"
                "$(chmod +x pppwn)"
                "$(mv pppwn /usr/bin)"
                echo "{\"output\":\"PPPwn installed\",\"pppwn\":true}"
                exit 0
            else
                echo "{\"output\":\"Cannot to get repos: $repo_refs\"}"
                exit 1
            fi
        else
            "$(wget -O /usr/bin/pppwn $repo_refs)"
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
        echo "\"root\":\"$root\","

        if [ -z "$latest_version" ]; then
            echo "\"update\":false,"
        else
            if [ "$latest_version" -gt "$current_version" ]; then
                echo "\"update\":true,"
            else
                echo "\"update\":false,"
            fi
        fi

        if command -v pppoe-server >/dev/null 2>&1; then
            if [ -n "$rspppoe" ]; then
                echo "\"pppoe\":\"running\","
            fi
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

            if [ -f /root/pw.conf ]; then
                source /root/pw.conf
            fi

            echo "\"adapter\":\"$interface\","
            echo "\"version\":\"$version\","
            echo "\"timeout\":\"$timeout\","

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

        set_params
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

        echo "{"
        echo "\"root\":\"$root\","
        echo "\"autorun\":$auto,"
        echo "\"adapter\":\"$adapter\","
        echo "\"version\":\"$version\","
        echo "\"timeout\":\"$timeout\""
        echo "}"

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

        set_params

        if [ "$auto" = 1 ]; then

            if ! grep -q "/root/run.sh" /etc/rc.local; then
                sed -i '/exit 0/d' /etc/rc.local
                echo "/root/run.sh &" >> /etc/rc.local
                echo "exit 0" >> /etc/rc.local
            fi

            chmod +x /etc/rc.local
            chmod +x /root/run.sh

        fi
        if [ "$auto" = 0 ]; then

            if grep -q "/root/run.sh" /etc/rc.local; then
                sed -i '/\/root\/run\.sh/d' /etc/rc.local
            fi

        fi

        echo "{"
        echo "\"root\":\"$root\","
        echo "\"autorun\":$auto,"
        echo "\"adapter\":\"$adapter\","
        echo "\"version\":\"$version\","
        echo "\"timeout\":\"$timeout\""
        echo "}"

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
        if [ -n "$rspppoe" ]; then
            /etc/init.d/pppoe-server stop
            echo "\"output\":\"PPPoE service stopped\","
        elif [ -z "$rspppoe" ]; then
            /etc/init.d/pppoe-server start
            echo "\"output\":\"PPPoE service started\","
        fi
        if [ -n "$rspppoe" ]; then
            echo "\"pppoe\":\"running\""
        else
            echo "\"pppoe\":\"inactive\""
        fi
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
