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

wget -O /tmp/main.zip https://github.com/CodeInvers3/PPPwn_ow/archive/refs/heads/main.zip
unzip /tmp/main.zip -d /tmp

if [ -f /tmp/main.zip ]; then
    rm /tmp/main.zip
fi

mv -f /tmp/PPPwn_ow-main/pppoe/ppp/pap-secrets /etc/ppp
mv -f /tmp/PPPwn_ow-main/pppoe/ppp/chap-secrets /etc/ppp
mv -f /tmp/PPPwn_ow-main/pppoe/ppp/pppoe-server-options /etc/ppp
mv -f /tmp/PPPwn_ow-main/pppoe/init.d/pppoe-server /etc/init.d
mv -f /tmp/PPPwn_ow-main/pppoe/config/pppoe /etc/config
mv -f /tmp/PPPwn_ow-main/www/pppwn /www
mv -f /tmp/PPPwn_ow-main/www/pppwn.html /www
mv -f /tmp/PPPwn_ow-main/www/cgi-bin/pw.cgi /www/cgi-bin
mv -f /tmp/PPPwn_ow-main/version /root/
mv -f /tmp/PPPwn_ow-main/pw.conf /root/
mv -f /tmp/PPPwn_ow-main/stage1 /root/
mv -f /tmp/PPPwn_ow-main/stage2 /root/
mv -f /tmp/PPPwn_ow-main/run.sh /root/

if [ -d /tmp/PPPwn_ow-main ]; then
    rm -r /tmp/PPPwn_ow-main
fi

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

echo "PPPwn web is hosted at http://192.168.8.1"
echo "Installation completed!"
exit 0