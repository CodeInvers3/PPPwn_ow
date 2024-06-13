#!/bin/sh /etc/rc.common

cd /tmp/

if ! command -v pppoe-server >/dev/null 2>&1; then
    opkg update
    opkg install rp-pppoe-server
fi
if [ -d /root/offsets ]; then
    rm -r /root/offsets
fi
if [ -d /www/pppwn ]; then
    rm -r /www/pppwn
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

mv -f /tmp/PPPwn_ow-main/pppoe/ppp/pap-secrets /etc/ppp
mv -f /tmp/PPPwn_ow-main/pppoe/ppp/chap-secrets /etc/ppp
mv -f /tmp/PPPwn_ow-main/pppoe/ppp/pppoe-server-options /etc/ppp
mv -f /tmp/PPPwn_ow-main/pppoe/init.d/pppoe-server /etc/init.d
mv -f /tmp/PPPwn_ow-main/pppoe/config/pppoe /etc/config

mv -f /tmp/PPPwn_ow-main/offsets /root/
mv -f /tmp/PPPwn_ow-main/www/pppwn /www
mv -f /tmp/PPPwn_ow-main/www/pppwn.html /www
mv -f /tmp/PPPwn_ow-main/www/cgi-bin/pw.cgi /www/cgi-bin
mv -f /tmp/PPPwn_ow-main/run.sh /root/

if [ -d /tmp/PPPwn_ow-main ]; then
    rm -r /tmp/PPPwn_ow-main
fi
if [ -f /root/main.zip ]; then
    rm -r /root/main.zip
fi

chmod +x /etc/init.d/pppoe-server
chmod +x /www/cgi-bin/pw.cgi

if ! grep -q "list device 'ppp+'" /etc/config/firewall; then
    sed -i "s/option name 'lan'/option name 'lan'\n\t list device 'ppp+'/" /etc/config/firewall
fi

/etc/init.d/pppoe-server start #initialize pppoe-server

echo "Installation completed!"
exit 0