#!/bin/sh /etc/rc.common

if [ -d ~/offsets ]; then
    rm -r ~/offsets
fi
if [ -d /www/pppwn ]; then
    rm -r /www/pppwn
fi
if [ -f /www/pppwn.html ]; then
    rm /www/pppwn.html
fi
if [ -f /www/cgi-bin/pw.cgi ]; then
    rm /www/cgi-bin/pw.cgi
fi
if [ -f ~/run.sh ]; then
    rm ~/run.sh
fi
mv -f ~/PPPwn_ow-main/offsets ~/
mv -f ~/PPPwn_ow-main/www/pppwn /www
mv -f ~/PPPwn_ow-main/www/pppwn.html /www
mv -f ~/PPPwn_ow-main/www/cgi-bin/pw.cgi /www/cgi-bin
mv -f ~/PPPwn_ow-main/run.sh ~/
rm -r PPPwn_ow-main main.zip
chmod +x /www/cgi-bin/pw.cgi
echo "Installation completed!"
exit 0