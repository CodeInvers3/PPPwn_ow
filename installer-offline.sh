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
if [ -f /usr/bin/pppwn ]; then
    rm /usr/bin/pppwn
fi

mv www/* /www
mv www/cgi-bin/pw.cgi /www/cgi-bin
mv stage1 /root
mv stage2 /root

mv version /root/version
mv run.sh /root/run.sh
mv pw.conf /root/pw.conf

mv -f pppoe/ppp/pap-secrets /etc/ppp
mv -f pppoe/ppp/chap-secrets /etc/ppp
mv -f pppoe/ppp/pppoe-server-options /etc/ppp
mv -f pppoe/init.d/pppoe-server /etc/init.d
mv -f pppoe/config/pppoe /etc/config

chmod +x /root/run.sh
chmod +x /www/cgi-bin/pw.cgi
chmod +x /etc/init.d/pppoe-server

if ! grep -q "list device 'ppp+'" /etc/config/firewall; then
    sed -i "s/option name 'lan'/option name 'lan'\n\t list device 'ppp+'/" /etc/config/firewall
fi

if [ ! -f /etc/rc.button/switch ]; then
    echo "#!/bin/sh\n action=on\n return 0" > /etc/rc.button/switch
    chmod +x /etc/rc.button/switch
fi
if ! grep -q "/root/run.sh" /etc/rc.button/switch; then
    sed -i "s/action=on/action=on\n\n\/root\/run\.sh/" /etc/rc.button/switch
fi
if [ -f pppwn ]; then
    mv pppwn /usr/bin
    chmod +x /usr/bin/pppwn
fi

/etc/init.d/pppoe-server start

rm README.md
rm installer.sh
rm installer-offline.sh

echo "PPPwn web is hosted at http://192.168.8.1/pppwn.html"
echo "--- INSTALLATION COMPLETED! ---"

cd /root
rm -rf ./PPPwn_ow

exit 0
