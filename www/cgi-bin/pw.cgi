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

    uci set pw.@params[0].root="$root"
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

    if [ -d /www/pppwn ]; then
        rm -rf /www/pppwn
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
    dir_name="$2"
    sp="$3"
    list_dir=$(ls "/$dir")

    for index in $list_dir; do
        
        echo "$sp{"
        echo "\"label\":\"$index\","
        if [ -f "/$dir/$index" ]; then
            echo "\"sub\":false,"
            echo "\"path\":\"$dir_name$index\""
        elif [ -d "/$dir/$index" ]; then
            echo "\"sub\":true,"
            echo "\"dir\":[$(ls_dir "$dir/$index" "$index/" "")]"
        fi

        if [ "$sp" = "" ]; then
            sp=","
        fi
        echo "}"

    done

}

#if ! [ "$token" = "$stoken" ] && ! [ "$task" = "state" ]; then
    #echo "Status: 400 Bad Request"
    #echo ""
    #echo "{\"output\":\"Invalid token\"}"
    #exit 1       
#fi

echo ""

case "$task" in

    "setup")

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

        echo ""
        echo "{"

        current_version=$(cat /root/version)
        latest_version=$(wget -qO- "https://raw.githubusercontent.com/CodeInvers3/PPPwn_ow/main/version" 2>/dev/null)

        echo "\"stored_token\":\"$stoken\","
        echo "\"chipname\":\"$(uname -m)\","
        echo "\"root\":\"$(uci get pw.@params[0].root)\","

        if [ -z "$latest_version" ]; then
            echo "\"update\":false,"
        else
            if [ "$latest_version" -gt "$current_version" ]; then
                echo "\"update\":true,"
            else
                echo "\"update\":false,"
            fi
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

            interface=$(uci get pw.@params[0].interface)
            version=$(uci get pw.@params[0].version)
            timeout=$(uci get pw.@params[0].timeout)

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
        if ls -l /etc/rc.d/ | grep -q pw; then
            echo "\"autorun\":true"
        else
            echo "\"autorun\":false"
        fi
        echo "}"

    ;;
    "start")

        set_params
        /etc/init.d/pw start

    ;;
    "stop")
        
        /etc/init.d/pw stop

        echo "{"
        echo "\"root\":\"$root\","
        echo "\"autorun\":$auto,"
        echo "\"adapter\":\"$adapter\","
        echo "\"version\":\"$version\","
        echo "\"timeout\":\"$timeout\""
        echo "}"

        exit 0

    ;;
    "params")

        set_params

        if [ "$auto" = 1 ]; then
            /etc/init.d/pw enable
        fi
        if [ "$auto" = 0 ]; then
            /etc/init.d/pw disable
        fi
        
        uci set uhttpd.usb.home="$root"
        uci commit uhttpd

        echo "{"
        echo "\"root\":\"$root\","
        echo "\"autorun\":$auto,"
        echo "\"adapter\":\"$adapter\","
        echo "\"version\":\"$version\","
        echo "\"timeout\":\"$timeout\""
        echo "}"

        exit 0

    ;;
    "update")
        
        rm_files
        
        "$(opkg update && opkg install rp-pppoe-common rp-pppoe-server)"
        wait

        mkdir /tmp/PPPwn_ow
        "$(wget -O /tmp/pw.tar https://raw.githubusercontent.com/CodeInvers3/codeinvers3.github.io/refs/heads/master/files/PPPwn_ow.tar &)"
        wait
        
        "$(tar -xvf /tmp/pw.tar -C /tmp/PPPwn_ow && rm /tmp/pw.tar)"
        mv -f /tmp/PPPwn_ow/etc/config/* /etc/config
        mv -f /tmp/PPPwn_ow/etc/init.d/* /etc/init.d
        mv -f /tmp/PPPwn_ow/etc/ppp/* /etc/ppp
        mv -f /tmp/PPPwn_ow/stage1 /root
        mv -f /tmp/PPPwn_ow/stage2 /root
        mv -f /tmp/PPPwn_ow/version /root
        mv -f /tmp/PPPwn_ow/www/pppwn /www
        mv -f /tmp/PPPwn_ow/www/pppwn.html /www
        mv -f /tmp/PPPwn_ow/www/cgi-bin/* /www/cgi-bin
        rm -r /tmp/PPPwn_ow
        chmod +x /etc/init.d/pw /etc/init.d/pppoe-server /www/cgi-bin/pw.cgi
        
        echo "{\"output\":\"Update completed\"}"
        
    ;;
    "remove")

        rm_files
        
        echo "{\"output\":\"Uninstalled\"}"

        exit 0
        
    ;;
    "connect")

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

    ;;
    "restartHttp")

        /etc/init.d/uhttpd restart
        exit 0

    ;;
    "payloads")
        
        root="$(uci get pw.@params[0].root)"
        
        echo "{"
        echo "\"file_list\":["
        if [ -d "$root/payloads" ]; then
            ls_dir "$root/payloads" "" ""
        fi
        echo "]"
        echo "}"

        exit 0

    ;;
    *)

        echo "Status: 400 Bad Request"
        echo ""
        echo "{\"output\":\"Invalid task\"}"
        exit 1

    ;;
esac