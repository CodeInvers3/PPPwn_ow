#!/bin/sh /etc/rc.common

if ! command -v pppoe-server >/dev/null 2>&1; then
    opkg update
    opkg install rp-pppoe-common
    opkg install rp-pppoe-server
fi

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
    rm -r /etc/ppp/chap-secrets
fi
if [ -f /etc/ppp/pap-secrets ]; then
    rm -r /etc/ppp/pap-secrets
fi
if [ -f /etc/ppp/pppoe-server-options ]; then
    rm -r /etc/ppp/pppoe-server-options
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

mv -f /tmp/PPPwn_ow-main/etc/config/pppoe /etc/config
mv -f /tmp/PPPwn_ow-main/etc/config/pw /etc/config
mv -f /tmp/PPPwn_ow-main/etc/init.d/pppoe-server /etc/init.d
mv -f /tmp/PPPwn_ow-main/etc/init.d/pw /etc/init.d
mv -f /tmp/PPPwn_ow-main/etc/ppp/pap-secrets /etc/ppp
mv -f /tmp/PPPwn_ow-main/etc/ppp/chap-secrets /etc/ppp
mv -f /tmp/PPPwn_ow-main/etc/ppp/pppoe-server-options /etc/ppp

mv -f /tmp/PPPwn_ow-main/www/pppwn /www
mv -f /tmp/PPPwn_ow-main/www/pppwn.html /www
mv -f /tmp/PPPwn_ow-main/www/cgi-bin/pw.cgi /www/cgi-bin
mv -f /tmp/PPPwn_ow-main/version /root
mv -f /tmp/PPPwn_ow-main/stage1 /root
mv -f /tmp/PPPwn_ow-main/stage2 /root

if [ -d /tmp/PPPwn_ow-main ]; then
    rm -r /tmp/PPPwn_ow-main
fi

chmod +x /etc/init.d/pw
chmod +x /etc/init.d/pppoe-server
chmod +x /www/cgi-bin/pw.cgi

if ! grep -q "list device 'ppp+'" /etc/config/firewall; then
    sed -i "s/option name 'lan'/option name 'lan'\n\t list device 'ppp+'/" /etc/config/firewall
fi

/etc/init.d/pppoe-server enable
/etc/init.d/pppoe-server start

rm /tmp/installer.sh

echo "PPPwn web is hosted at http://localhost/pppwn.html"
echo "--- INSTALLATION COMPLETED! ---"
exit 0