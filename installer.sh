#!/bin/sh /etc/rc.common

installer_setup(){
    
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
    if [ -d /www/pppwn ]; then
        rm -r /www/pppwn
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
    if [ -f /www/pppwn.html ]; then
        rm /www/pppwn.html
    fi
    if [ -f /www/cgi-bin/pw.cgi ]; then
        rm /www/cgi-bin/pw.cgi
    fi

    echo "Confirm installation type."

    if [ "$1" = "offline" ]; then

        read -p "Complete installacion? y/n: " optyn

        if [ "$optyn" = "y" ]; then

            if [ -f rp-pppoe-common.ipk ]; then
                opkg install rp-pppoe-common.ipk
            fi
            if [ -f rp-pppoe-server.ipk ]; then
                opkg install rp-pppoe-server.ipk
                
                mv -f etc/config/firewall /etc/config
                mv -f etc/config/pppoe /etc/config
                mv -f etc/init.d/pppoe-server /etc/init.d
                mv -f etc/ppp/pap-secrets /etc/ppp
                mv -f etc/ppp/chap-secrets /etc/ppp
                mv -f etc/ppp/pppoe-server-options /etc/ppp
                
            fi

            mv -f www/pppwn /www
            mv -f www/pppwn.html /www
            mv -f www/cgi-bin/pw.cgi /www/cgi-bin

            chmod +x /etc/init.d/pppoe-server
            chmod +x /www/cgi-bin/pw.cgi

            /etc/init.d/pppoe-server enable
            /etc/init.d/pppoe-server start
            
        else
        
            echo "Select ethernet connection"
            echo "1) eth0"
            echo "2) br-lan"

            read -p "Select option: " opt1
            
            adapter=""

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
            if grep -q "interface=" "etc/config/pw"; then
                sed -i "s/interface=.*/interface=\"$adapter\"/" "etc/config/pw"
            fi

            echo "Set firmware version"
            echo "1) 9.00"
            echo "2) 9.50"
            echo "3) 9.51"
            echo "4) 9.60"
            echo "5) 10.00"
            echo "6) 10.01"
            echo "7) 11.00"

            read -p "Select option: " opt2

            version=1100

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
            if grep -q "version=" "etc/config/pw"; then
                sed -i "s/version=.*/version=\"$version\"/" "etc/config/pw"
            fi
            if grep -q "stage1=" "etc/config/pw"; then
                sed -i "s/stage1=.*/stage1=\"\/root\/stage1\/$version.bin\"/" "etc/config/pw"
            fi
            if grep -q "stage2=" "etc/config/pw"; then
                sed -i "s/stage2=.*/stage2=\"\/root\/stage2\/$version.bin\"/" "etc/config/pw"
            fi

            read -p "Set timeout 0 to 60 (default 0): " timeout

            if [ -z "$timeout" ]; then
                timeout=0
            fi
            if grep -q "timeout=" "etc/config/pw"; then
                sed -i "s/timeout=.*/timeout=\"$timeout\"/" "etc/config/pw"
            fi

        fi

        mv -f etc/config/pw /etc/config
        mv -f etc/init.d/pw /etc/init.d
        mv -f stage1 /root
        mv -f stage2 /root
        mv -f version /root
        
        chmod +x /etc/init.d/pw

        if [ -f pppwn ]; then
            mv -f pppwn /usr/sbin
            chmod +x /usr/sbin/pppwn
        fi

        rm README.md
        rm installer.sh

        if [ -d /root/PPPwn_ow ]; then
            rm -rf /root/PPPwn_ow
        fi
        if [ -d /root/PPPwn_ow-main ]; then
            rm -rf /root/PPPwn_ow-main
        fi

    elif [ "$1" = "download" ]; then

        if ! command -v pppoe-server >/dev/null 2>&1; then
            opkg update
            opkg install rp-pppoe-common
            opkg install rp-pppoe-server
        fi

        wget -O /tmp/main.zip https://github.com/CodeInvers3/PPPwn_ow/archive/refs/heads/main.zip
        unzip /tmp/main.zip -d /tmp

        if [ -f /tmp/main.zip ]; then
            rm /tmp/main.zip
        fi

        mv -f /tmp/PPPwn_ow-main/etc/config/firewall /etc/config
        mv -f /tmp/PPPwn_ow-main/etc/config/pppoe /etc/config
        mv -f /tmp/PPPwn_ow-main/etc/config/pw /etc/config
        mv -f /tmp/PPPwn_ow-main/etc/init.d/pppoe-server /etc/init.d
        mv -f /tmp/PPPwn_ow-main/etc/init.d/pw /etc/init.d
        mv -f /tmp/PPPwn_ow-main/etc/ppp/pap-secrets /etc/ppp
        mv -f /tmp/PPPwn_ow-main/etc/ppp/chap-secrets /etc/ppp
        mv -f /tmp/PPPwn_ow-main/etc/ppp/pppoe-server-options /etc/ppp

        read -p "Complete installation? y/n: " optyn

        if [ "$optyn" = "y" ]; then
            mv -f /tmp/PPPwn_ow-main/www/pppwn /www
            mv -f /tmp/PPPwn_ow-main/www/pppwn.html /www
            mv -f /tmp/PPPwn_ow-main/www/cgi-bin/pw.cgi /www/cgi-bin
            chmod +x /www/cgi-bin/pw.cgi
        else
        
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
            if grep -q "interface=" "/etc/config/pw"; then
                sed -i "s/interface=.*/interface=\"$adapter\"/" "/etc/config/pw"
            fi

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
            if grep -q "version=" "/etc/config/pw"; then
                sed -i "s/version=.*/version=\"$version\"/" "/etc/config/pw"
            fi
            if grep -q "stage1=" "/etc/config/pw"; then
                sed -i "s/stage1=.*/stage1=\"\/root\/stage1\/$version.bin\"/" "/etc/config/pw"
            fi
            if grep -q "stage2=" "/etc/config/pw"; then
                sed -i "s/stage2=.*/stage2=\"\/root\/stage2\/$version.bin\"/" "/etc/config/pw"
            fi

            read -p "Set timeout 0 to 60 (default 0): " timeout

            if [ -z "$timeout" ]; then
                timeout=0
            fi
            if grep -q "timeout=" "/etc/config/pw"; then
                sed -i "s/timeout=.*/timeout=\"$timeout\"/" "/etc/config/pw"
            fi
        
        fi

        mv -f /tmp/PPPwn_ow-main/version /root
        mv -f /tmp/PPPwn_ow-main/stage1 /root
        mv -f /tmp/PPPwn_ow-main/stage2 /root

        chmod +x /etc/init.d/pw
        chmod +x /etc/init.d/pppoe-server

        
        if [ "$optyn" = "n" ]; then
            /etc/init.d/pw enable
        fi
        if [ -d /tmp/PPPwn_ow-main ]; then
            rm -r /tmp/PPPwn_ow-main
        fi

        rm /tmp/installer.sh
    
    fi

    echo "PPPwn web is hosted at http://ip_address/pppwn.html"
    echo "--- INSTALLATION COMPLETED! ---"
    exit 0

    break
}

echo "PPPwn installer"
echo "1) Offline (Require packages files)"
echo "2) Download (Require internet connection)"
echo "3) Cancel and exit"

while true; do

    read -p "Select option: " opt
    
    case $opt in
        1)
            installer_setup "offline"
            continue
            ;;
        2)
            if ping -c 1 www.google.com >/dev/null 2>&1; then
                installer_setup "download"
            else
                echo "Require internet connection."
                break
            fi
            continue
            ;;
        3)
            echo "Finishing..."
            break
            ;;
        *)
            echo "Invalid option, please select a valid option."
            ;;
    esac

done
