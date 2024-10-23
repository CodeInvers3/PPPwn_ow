#!/bin/sh /etc/rc.common

if [ -f /etc/config/pppoe ]; then
    rm -r /etc/config/pppoe
fi
if [ -f /etc/config/pw ]; then
    rm -r /etc/config/pw
fi
if [ -f /etc/init.d/pppoe-server ]; then
    rm -r /etc/init.d/pppoe-server
fi
if [ -f /etc/init.d/pw ]; then
    rm -r /etc/init.d/pw
fi
if [ -f /etc/ppp/chap-secrets ]; then
    rm -f /etc/ppp/chap-secrets
fi
if [ -f /etc/ppp/pap-secrets ]; then
    rm -f /etc/ppp/pap-secrets
fi
if [ -f /etc/ppp/pppoe-server-options ]; then
    rm -f /etc/ppp/pppoe-server-options
fi

if [ -f /tmp/main.zip ]; then
    rm -r /tmp/main.zip
fi
if [ -d /root/offsets ]; then
    rm -r /root/offsets
fi
if [ -d /root/stage1 ]; then
    rm -r /root/stage1
fi
if [ -d /root/stage2 ]; then
    rm -r /root/stage2
fi
if [ -d /www/assets ]; then
    rm -r /www/assets
fi
if [ -f /www/cgi-bin/pw.cgi ]; then
    rm /www/cgi-bin/pw.cgi
fi
if [ -f /www/pppwn.html ]; then
    rm /www/pppwn.html
fi
if [ -f /root/pw.conf ]; then
    rm /root/pw.conf
fi
if [ -f /root/version ]; then
    rm /root/version
fi
if [ -f /root/run.sh ]; then
    rm /root/run.sh
fi

installer_setup(){

    dir_root=""

    if [ "$1" = "download" ]; then
        
        dir_root="/tmp/PPPwn_ow-main/"
        
        wget -O /tmp/main.zip https://github.com/CodeInvers3/PPPwn_ow/archive/refs/heads/main.zip
        unzip /tmp/main.zip -d /tmp
        rm /tmp/main.zip
        
    fi

    echo "Confirm installation type."
    read -p "Complete installacion? y/n: " optyn

    if [ "$optyn" = "y" ]; then

        if [ "$1" = "offline" ]; then

            if [ -f rp-pppoe-common*.ipk ]; then
                opkg install rp-pppoe-common*.ipk
            fi
            if [ -f rp-pppoe-server*.ipk ]; then
                opkg install rp-pppoe-server*.ipk
            fi
        fi

        if [ "$1" = "download" ]; then

            if ! command -v pppoe-server >/dev/null 2>&1; then
                opkg update
                opkg install rp-pppoe-common
                opkg install rp-pppoe-server
            fi

        fi

        mv -f ${dir_root}etc/config/pw /etc/config
        mv -f ${dir_root}etc/config/pppoe /etc/config
        mv -f ${dir_root}etc/init.d/pppoe-server /etc/init.d
        mv -f ${dir_root}etc/ppp/pap-secrets /etc/ppp
        mv -f ${dir_root}etc/ppp/chap-secrets /etc/ppp
        mv -f ${dir_root}etc/ppp/pppoe-server-options /etc/ppp
        mv -f ${dir_root}www/cgi-bin/pw.cgi /www/cgi-bin/
        mv -f ${dir_root}www/pppwn.html /www/
        mv -f ${dir_root}www/assets /www/

        chmod +x /etc/init.d/pppoe-server /www/cgi-bin/pw.cgi

        uci del_list firewall.@zone[0].device='ppp+'
        uci add_list firewall.@zone[0].device='ppp+'
        uci set firewall.@zone[1].input='ACCEPT'
        uci commit firewall
        
        /etc/init.d/pppoe-server enable
        /etc/init.d/pppoe-server start
        
    else

        mtype=$(uname -m)
        echo "Download PPPWN that is compatible with your chip."
        echo "Your machine type: $mtype"
        echo "1) aarch64-linux-musl"
        echo "2) arm-linux-musleabi(cortex_a7)"
        echo "3) arm-linux-musleabi(pi_zero_w)"
        echo "4) arm-linux-musleabi(mpcorenovfp)"
        echo "5) x86_64-linux-musl"
        echo "6) mipsel-linux-musl"
        echo "7) mips-linux-musl"

        while true; do
        read -p "Select a option: " optdwn
        case $optdwn in
            1)
                repo_ref="https://raw.githubusercontent.com/CodeInvers3/codeinvers3.github.io/master/custom/stored/aarch64-linux-musl.tar.gz"
                break
                ;;
            2)
                repo_ref="https://raw.githubusercontent.com/CodeInvers3/codeinvers3.github.io/master/custom/stored/arm-linux-musleabi(cortex_a7).tar.gz"
                break
                ;;
            3)
                repo_ref="https://raw.githubusercontent.com/CodeInvers3/codeinvers3.github.io/master/custom/stored/arm-linux-musleabi(pi_zero_w).tar.gz"
                break
                ;;
            4)
                repo_ref="https://raw.githubusercontent.com/CodeInvers3/codeinvers3.github.io/master/custom/stored/arm-linux-musleabi(mpcorenovfp).tar.gz"
                break
                ;;
            5)
                repo_ref="https://raw.githubusercontent.com/CodeInvers3/codeinvers3.github.io/master/custom/stored/x86_64-linux-musl.tar.gz"
                break
                ;;
            6)
                repo_ref="https://raw.githubusercontent.com/CodeInvers3/codeinvers3.github.io/master/custom/stored/mipsel-linux-musl.tar.gz"
                break
                ;;
            7)
                repo_ref="https://raw.githubusercontent.com/CodeInvers3/codeinvers3.github.io/master/custom/stored/mips-linux-musl.tar.gz"
                break
                ;;
            *)
                echo "Invalid selection, retry again."
                ;;
        esac
        done
        
        echo "Select ethernet connection"
        echo "1) eth0"
        echo "2) br-lan"

        read -p "Select option: " opt1

        case $opt1 in
            1)
                adapter="eth0"
                ;;
            2)
                adapter="br-lan"
                ;;
            *)
                adapter="br-lan"
                ;;
        esac

        echo "Set firmware version"
        echo "1) 9.00"
        echo "2) 9.50"
        echo "3) 9.51"
        echo "4) 9.60"
        echo "5) 10.00"
        echo "6) 10.01"
        echo "7) 11.00"

        read -p "Select option: " opt2

        case $opt2 in
            1)
                version=900
                ;;
            2)
                version=950
                ;;
            3)
                version=951
                ;;
            4)
                version=960
                ;;
            5)
                version=1000
                ;;
            6)
                version=1001
                ;;
            7)
                version=1100
                ;;
            *)
                version=1100
                ;;
        esac

        read -p "Set timeout 0 to 60 (default 0): " timeout

        if [ -z "$timeout" ]; then
            timeout=0
        fi

        wget -O ${dir_root}pppwn.tar.gz $repo_ref
        tar -xvzf ${dir_root}pppwn.tar.gz -C $dir_root
        rm ${dir_root}pppwn.tar.gz

        mv -f ${dir_root}etc/config/pw /etc/config

        uci set pw.@params[0].interface="$adapter"
        uci set pw.@params[0].version="$version"
        uci set pw.@params[0].timeout="$timeout"
        uci set pw.@params[0].stage1="/root/stage1/$version.bin"
        uci set pw.@params[0].stage2="/root/stage2/$version.bin"
        uci commit pw

    fi

    if [ -f ${dir_root}pppwn ]; then
        mv -f ${dir_root}pppwn /usr/sbin
        chmod +x /usr/sbin/pppwn
    fi
    mv -f ${dir_root}etc/init.d/pw /etc/init.d
    mv -f ${dir_root}version /root
    mv -f ${dir_root}stage1 /root
    mv -f ${dir_root}stage2 /root

    chmod +x /etc/init.d/pw

    if [ "$optyn" = "n" ]; then
        /etc/init.d/pw enable
    fi

    if [ "$1" = "offline" ]; then

        if [ -d /root/PPPwn_ow ]; then
            rm -rf /root/PPPwn_ow
        fi
        if [ -d /root/PPPwn_ow-main ]; then
            rm -rf /root/PPPwn_ow-main
        fi

    fi

    if [ "$1" = "download" ]; then

        rm /tmp/installer.sh
        if [ -d /tmp/PPPwn_ow-main ]; then
            rm -r /tmp/PPPwn_ow-main
        fi
        
    fi

    echo "PPPwn web is hosted at http://ip_address/pppwn.html"
    echo "--- INSTALLATION COMPLETED! ---"

    exit 0

    break
}

echo "PPPwn installer"
echo "The complete installation includes settings from a web interface."
echo "the minimal installation only includes the necessary executables."

if ping -c 1 www.google.com >/dev/null 2>&1; then
    if [ -f /tmp/installer.sh ]; then
        installer_setup "download"
    else
        installer_setup "offline"
    fi
else
    installer_setup "offline"
fi