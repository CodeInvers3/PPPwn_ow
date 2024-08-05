#!/bin/sh

if ! command -v pppoe-server >/dev/null 2>&1; then
    opkg update
    opkg install rp-pppoe-server
fi

if [ -d /etc/ppp ]; then
    rm -r /etc/ppp
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
if [ -f /etc/init.d/pppoe-server ]; then
    rm /etc/init.d/pppoe-server
fi
if [ -f /etc/config/pppoe ]; then
    rm /etc/config/pppoe
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

if [ ! -d /etc/ppp ]; then
    mkdir /etc/ppp
fi
if [ ! -d /etc/init.d ]; then
    mkdir /etc/init.d
fi
if [ ! -d /etc/config ]; then
    mkdir /etc/config
fi

mv ./www/* /www
mv ./www/cgi-bin/pw.cgi /www/cgi-bin/pw.cgi
mv ./stage1 /root
mv ./stage2 /root

mv ./version /root/version
mv ./run.sh /root/run.sh
mv ./pw.conf /root/pw.conf

mv ./pppoe/ppp/pap-secrets /etc/ppp/pap-secrets
mv ./pppoe/ppp/chap-secrets /etc/ppp/chap-secrets
mv ./pppoe/ppp/pppoe-server-options /etc/ppp/pppoe-server-options
mv ./pppoe/init.d/pppoe-server /etc/init.d/pppoe-server
mv ./pppoe/config/pppoe /etc/config/pppoe

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

rm ./README.md
rm ./installer.sh
rm ./installer-offline.sh

cd ..
rm -rf PPPwn_ow

echo "PPPwn web is hosted at http://192.168.8.1/pppwn.html"
echo "--- INSTALLATION COMPLETED! ---"
cd /

exit 0
