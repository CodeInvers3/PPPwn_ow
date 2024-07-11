#!/bin/sh /etc/rc.common

if ! command -v pppoe-server >/dev/null 2>&1; then
    opkg update
    opkg install rp-pppoe-server
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

mkdir /www/pppwn
mkdir /root/stage1
mkdir /root/stage2
mkdir /www/pppwn/assets
mkdir /www/pppwn/assets/js
mkdir /www/pppwn/assets/css

wget -O /etc/ppp/pap-secrets https://raw.githubusercontent.com/CodeInvers3/PPPwn_ow/main/pppoe/ppp/pap-secrets
wget -O /etc/ppp/chap-secrets https://raw.githubusercontent.com/CodeInvers3/PPPwn_ow/main/pppoe/ppp/chap-secrets
wget -O /etc/ppp/pppoe-server-options https://raw.githubusercontent.com/CodeInvers3/PPPwn_ow/main/pppoe/ppp/pppoe-server-options
wget -O /etc/init.d/pppoe-server https://raw.githubusercontent.com/CodeInvers3/PPPwn_ow/main/pppoe/init.d/pppoe-server
wget -O /etc/config/pppoe https://github.com/CodeInvers3/PPPwn_ow/raw/main/pppoe/config/pppoe
wget -O /www/pppwn/assets/css/custom.css https://github.com/CodeInvers3/PPPwn_ow/raw/main/www/pppwn/assets/css/custom.css
wget -O /www/pppwn/assets/css/base.css https://github.com/CodeInvers3/PPPwn_ow/raw/main/www/pppwn/assets/css/base.css
wget -O /www/pppwn/assets/js/backbone-min.js https://github.com/CodeInvers3/PPPwn_ow/raw/main/www/pppwn/assets/js/backbone-min.js
wget -O /www/pppwn/assets/js/jquery.min.js https://github.com/CodeInvers3/PPPwn_ow/raw/main/www/pppwn/assets/js/jquery.min.js
wget -O /www/pppwn/assets/js/plugin.modal.js https://github.com/CodeInvers3/PPPwn_ow/raw/main/www/pppwn/assets/js/plugin.modal.js
wget -O /www/pppwn/assets/js/underscore-min.js https://github.com/CodeInvers3/PPPwn_ow/raw/main/www/pppwn/assets/js/underscore-min.js
wget -O /www/pppwn/main.js https://github.com/CodeInvers3/PPPwn_ow/blob/main/www/pppwn/main.js
wget -O /www/pppwn.html https://github.com/CodeInvers3/PPPwn_ow/raw/main/www/pppwn.html
wget -O /www/cgi-bin/pw.cgi https://github.com/CodeInvers3/PPPwn_ow/raw/main/www/cgi-bin/pw.cgi
wget -O /root/stage1/1000.bin https://github.com/CodeInvers3/PPPwn_ow/raw/main/stage1/1000.bin
wget -O /root/stage1/1001.bin https://github.com/CodeInvers3/PPPwn_ow/raw/main/stage1/1001.bin
wget -O /root/stage1/1100.bin https://github.com/CodeInvers3/PPPwn_ow/raw/main/stage1/1100.bin
wget -O /root/stage1/900.bin https://github.com/CodeInvers3/PPPwn_ow/raw/main/stage1/900.bin
wget -O /root/stage1/950.bin https://github.com/CodeInvers3/PPPwn_ow/raw/main/stage1/950.bin
wget -O /root/stage1/951.bin https://github.com/CodeInvers3/PPPwn_ow/raw/main/stage1/951.bin
wget -O /root/stage1/960.bin https://github.com/CodeInvers3/PPPwn_ow/raw/main/stage1/960.bin
wget -O /root/stage2/1000.bin https://github.com/CodeInvers3/PPPwn_ow/raw/main/stage2/1000.bin
wget -O /root/stage2/1001.bin https://github.com/CodeInvers3/PPPwn_ow/raw/main/stage2/1001.bin
wget -O /root/stage2/1100.bin https://github.com/CodeInvers3/PPPwn_ow/raw/main/stage2/1100.bin
wget -O /root/stage2/900.bin https://github.com/CodeInvers3/PPPwn_ow/raw/main/stage2/900.bin
wget -O /root/stage2/950.bin https://github.com/CodeInvers3/PPPwn_ow/raw/main/stage2/950.bin
wget -O /root/stage2/951.bin https://github.com/CodeInvers3/PPPwn_ow/raw/main/stage2/951.bin
wget -O /root/stage2/960.bin https://github.com/CodeInvers3/PPPwn_ow/raw/main/stage2/960.bin
wget -O /root/pw.conf https://github.com/CodeInvers3/PPPwn_ow/raw/main/pw.conf
wget -O /root/run.sh https://github.com/CodeInvers3/PPPwn_ow/raw/main/run.sh
wget -O /root/version https://github.com/CodeInvers3/PPPwn_ow/raw/main/version

chmod +x /root/run.sh
chmod +x /www/cgi-bin/pw.cgi
chmod +x /etc/init.d/pppoe-server

if ! grep -q "list device 'ppp+'" /etc/config/firewall; then
    sed -i "s/option name 'lan'/option name 'lan'\n\t list device 'ppp+'/" /etc/config/firewall
fi

if ! grep -q "/root/run.sh" /etc/rc.button/switch; then
    sed -i "s/action=on/action=on\n\n\/root\/run\.sh/" /etc/rc.button/switch
fi

/etc/init.d/pppoe-server start

rm /tmp/installer.sh

echo "PPPwn web is hosted at http://192.168.8.1/pppwn.html"
echo "--- INSTALLATION COMPLETED! ---"
exit 0