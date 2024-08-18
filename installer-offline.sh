#!/bin/sh

if [ -f rp-pppoe-common.ipk ]; then
    opkg install rp-pppoe-common.ipk
fi
if [ -f rp-pppoe-server.ipk ]; then
    opkg install rp-pppoe-server.ipk
fi

if [ -f /etc/config/firewall ]; then
    rm -r /etc/config/firewall
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
    rm -f /etc/ppp/chap-secrets
fi
if [ -f /etc/ppp/pap-secrets ]; then
    rm -f /etc/ppp/pap-secrets
fi
if [ -f /etc/ppp/pppoe-server-options ]; then
    rm -f /etc/ppp/pppoe-server-options
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
if [ -f /usr/sbin/pppwn ]; then
    rm /usr/sbin/pppwn
fi
if [ -f /etc/ppp ]; then
    rm -rf /etc/ppp
    mkdir /etc/ppp
fi

mv -f etc/config/firewall /etc/config
mv -f etc/config/pppoe /etc/config
mv -f etc/config/pw /etc/config
mv -f etc/init.d/pppoe-server /etc/init.d
mv -f etc/init.d/pw /etc/init.d
mv -f etc/ppp/pap-secrets /etc/ppp
mv -f etc/ppp/chap-secrets /etc/ppp
mv -f etc/ppp/pppoe-server-options /etc/ppp

mv -f www/pppwn /www
mv -f www/pppwn.html /www
mv -f www/cgi-bin/pw.cgi /www/cgi-bin
mv -f stage1 /root
mv -f stage2 /root
mv -f version /root

chmod +x /etc/init.d/pw
chmod +x /etc/init.d/pppoe-server
chmod +x /www/cgi-bin/pw.cgi

if [ -f pppwn ]; then
    mv -f pppwn /usr/sbin
    chmod +x /usr/sbin/pppwn
fi

if ! grep -q "list device 'ppp+'" /etc/config/firewall; then
    sed -i "s/option name 'lan'/option name 'lan'\n\t list device 'ppp+'/" /etc/config/firewall
fi

/etc/init.d/pppoe-server enable
/etc/init.d/pppoe-server start

rm README.md
rm installer.sh
rm installer-offline.sh

echo "PPPwn web is hosted at http://localhost/pppwn.html"
echo "--- INSTALLATION COMPLETED! ---"

cd ..
rm -rf PPPwn_ow

exit 0