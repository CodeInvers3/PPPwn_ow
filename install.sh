#!/bin/sh /etc/rc.common

mv -f ~/PPPwn_ow-main/www/pppwn/* /www
mv -f ~/PPPwn_ow-main/www/pppwn.html /www
mv -f ~/PPPwn_ow-main/www/cgi-bin/wpwn.cgi /www/cgi-bin
rm -r ~/PPPwn_ow-main/www
mv -f ~/PPPwn_ow-main/run.sh ~/
rm -r PPPwn_ow-main main

chmod +x /www/cgi-bin/wpwn.cgi