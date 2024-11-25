#!/bin/sh

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
adapter=$(echo "$adapter" | sed 's/+/ /g')
version=$(echo $postData | sed -n 's/^.*version=\([^&]*\).*$/\1/p' | sed "s/%20/ /g")
stage1=$(echo $postData | sed -n 's/^.*stage1=\([^&]*\).*$/\1/p' | sed "s/%20/ /g")
stage1=$(echo "$stage1" | sed 's/%2F/\//g')
stage2=$(echo $postData | sed -n 's/^.*stage2=\([^&]*\).*$/\1/p' | sed "s/%20/ /g")
stage2=$(echo "$stage2" | sed 's/%2F/\//g')
timeout=$(echo $postData | sed -n 's/^.*timeout=\([^&]*\).*$/\1/p' | sed "s/%20/ /g")
auto=$(echo $postData | sed -n 's/^.*auto=\([^&]*\).*$/\1/p' | sed "s/%20/ /g")
retry=$(echo $postData | sed -n 's/^.*retry=\([^&]*\).*$/\1/p' | sed "s/%20/ /g")
sleep=$(echo $postData | sed -n 's/^.*sleep=\([^&]*\).*$/\1/p' | sed "s/%20/ /g")
task=$(echo $postData | sed -n 's/^.*task=\([^&]*\).*$/\1/p' | sed "s/%20/ /g")
option=$(echo $postData | sed -n 's/^.*option=\([^&]*\).*$/\1/p' | sed "s/%20/ /g")
path=$(echo $postData | sed -n 's/^.*path=\([^&]*\).*$/\1/p' | sed "s/%20/ /g")
path=$(echo "$path" | sed 's/%2F/\//g')

if [ -z "$timeout" ]; then
    timeout=0
fi
if [ -z "$path" ]; then
    path="/payloads"
fi

set_params(){

    uci set pw.@params[0].path="$path"
    uci set pw.@params[0].retry="$retry"
    uci set pw.@params[0].sleep="$sleep"
    uci set pw.@params[0].interface="$adapter"
    uci set pw.@params[0].version="$version"
    uci set pw.@params[0].timeout="$timeout"
    uci set pw.@params[0].stage1="$stage1"
    uci set pw.@params[0].stage2="$stage2"
    uci commit pw

}

rm_files(){

    "$(opkg remove rp-pppoe-server && rp-pppoe-common)"

    if [ -f /etc/init.d/pppoe-server ]; then
        rm /etc/init.d/pppoe-server
    fi
    if [ -f /etc/config/pppoe ]; then
        rm /etc/config/pppoe
    fi
    if [ -f /etc/ppp/chap-secrets ]; then
        rm /etc/ppp/chap-secrets
    fi
    if [ -f /etc/ppp/pap-secrets ]; then
        rm /etc/ppp/pap-secrets
    fi
    if [ -f /etc/ppp/pppoe-server-options ]; then
        rm /etc/ppp/pppoe-server-options
    fi
    
    rm -f /usr/sbin/pppwn /etc/init.d/pw /etc/config/pw && rm -rf /root/*

    if [ -d /www/assets ]; then
        rm -rf /www/assets
    fi
    if [ -f /www/pppwn.html ]; then
        rm -f /www/pppwn.html
    fi
    if [ -f /www/cgi-bin/pw.cgi ]; then
        rm -f /www/cgi-bin/pw.cgi
    fi

}

ls_dir(){

    dir="$1"
    path="$2"
    dirpath="$1$2"
    sp="$3"
    list_dir=$(ls "$dirpath")

    for index in $list_dir; do
        
        echo "$sp{"
        echo "\"label\":\"$(basename $index | sed 's/\.bin$//')\","
        if [ -f "$dirpath/$index" ]; then
            echo "\"sub\":false,"
            echo "\"path\":\"$dirpath/$index\""
        elif [ -d "$dirpath/$index" ]; then
            echo "\"sub\":true,"
            echo "\"dir\":[$(ls_dir "$dirpath" "/$index" "")]"
        fi

        if [ "$sp" = "" ]; then
            sp=","
        fi
        echo "}"

    done

}

case "$task" in

    "setup")

        echo "Content-Type: application/json"
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
                "$(mv pppwn /usr/sbin)"
                echo "{\"output\":\"PPPwn installed\",\"pppwn\":true}"
                exit 0
            else
                echo "{\"output\":\"Cannot to get repos: $repo_refs\"}"
                exit 1
            fi
        else
            "$(wget -O /usr/sbin/pppwn $repo_refs)"
            "$(chmod +x /usr/sbin/pppwn)"
            echo "{\"output\":\"PPPwn installed\",\"pppwn\":true}"
            exit 0
        fi

    ;;
    "state")

        echo "Content-Type: application/json"
        echo ""

        echo "{"

        current_version=$(cat /root/version)
        latest_version=$(wget -qO- "https://raw.githubusercontent.com/CodeInvers3/PPPwn_ow/main/version" 2>/dev/null)

        echo "\"stored_token\":\"$stoken\","
        echo "\"chipname\":\"$(uname -m)\","
        echo "\"path\":\"$(uci get pw.@params[0].path)\","

        if [ "$latest_version" -gt "$current_version" ]; then
            if ! [ -f /tmp/updater.sh ]; then
                "$(wget -O /tmp/updater.sh https://raw.githubusercontent.com/CodeInvers3/codeinvers3.github.io/refs/heads/master/files/updater.sh)"
                chmod +x /tmp/updater.sh
            fi
            echo "\"update\":true,"
        else
            echo "\"update\":false,"
        fi

        if pgrep pppoe-server > /dev/null; then
            echo "\"pppoe\":true,"
        else
            echo "\"pppoe\":false,"
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

            echo "\"retry\":\"$(uci get pw.@params[0].retry)\","
            echo "\"sleep\":\"$(uci get pw.@params[0].sleep)\","
            echo "\"adapter\":\"$(uci get pw.@params[0].interface)\","
            echo "\"version\":\"$(uci get pw.@params[0].version)\","
            echo "\"timeout\":\"$(uci get pw.@params[0].timeout)\","

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
        if ls -l /etc/rc.d/ | grep -q pw; then
            echo "\"autorun\":\"yes\""
        else
            echo "\"autorun\":\"no\""
        fi
        echo "}"

    ;;
    "start")

        set_params
        /etc/init.d/pw start

    ;;
    "stop")

        echo "Content-Type: application/json"
        echo ""
        
        /etc/init.d/pw stop

        echo "{"
        echo "\"autorun\":\"$auto\","
        echo "\"retry\":\"$retry\","
        echo "\"sleep\":\"$sleep\","
        echo "\"path\":\"$path\","
        echo "\"adapter\":\"$adapter\","
        echo "\"version\":\"$version\","
        echo "\"timeout\":\"$timeout\""
        echo "}"

        exit 0

    ;;
    "save")

        echo "Content-Type: application/json"
        echo ""

        set_params

        if [ "$auto" = "yes" ]; then
            /etc/init.d/pw enable
        fi
        if [ "$auto" = "no" ]; then
            /etc/init.d/pw disable
        fi

        echo "{"
        echo "\"autorun\":\"$auto\","
        echo "\"retry\":\"$retry\","
        echo "\"sleep\":\"$sleep\","
        echo "\"path\":\"$path\","
        echo "\"adapter\":\"$adapter\","
        echo "\"version\":\"$version\","
        echo "\"timeout\":\"$timeout\""
        echo "}"

        exit 0

    ;;
    "update")

        echo "Content-Type: application/json"
        echo ""
        
        #/etc/init.d/pw update
        "$(/tmp/updater.sh)"
        wait

        echo "{\"output\":\"Updated!\"}"

        exit 0
        
    ;;
    "remove")

        echo "Content-Type: application/json"
        echo ""

        rm_files
        
        echo "{\"output\":\"Uninstalled\"}"

        exit 0
        
    ;;
    "reconnect")

        echo "Content-Type: application/json"
        echo ""

        echo "{"
        if pgrep pppoe-server > /dev/null; then
            /etc/init.d/pppoe-server stop
            echo "\"output\":\"PPPoE service stopped\","
        elif ! pgrep pppoe-server > /dev/null; then
            /etc/init.d/pppoe-server start
            echo "\"output\":\"PPPoE service started\","
        fi
        if pgrep pppoe-server > /dev/null; then
            echo "\"pppoe\":true"
        else
            echo "\"pppoe\":false"
        fi
        echo "}"

        exit 0

    ;;
    "payloads")

        echo "Content-Type: application/json"
        echo ""
        
        path="$(uci get pw.@params[0].path)"
        
        echo "{"
        echo "\"file_list\":["
        if [ -d "/www$path" ]; then
            ls_dir "/www" "$path" ""
        fi
        echo "]"
        echo "}"

        exit 0

    ;;
    *)

        echo "Status: 400 Bad Request"
        echo ""
        echo "Invalid task"
        exit 1

    ;;
esac