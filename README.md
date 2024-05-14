# PPPwn_ow
Una adaptación del código de stooged para que funcione con PPPwn_cpp

Esto sirve para que arranque en un modem que tenga un sistema OpenWrt instalado

- Se requiere putty para acceder al sistema del modem
- Necesitas descargar los payload y tener los stage1.bin y stage2.bin para el FW correspondiente
- Descarga pppwn para el sistema que tenga tu modem/mini-router puedes verificarlo con el comando "uname -m"
- La instalación es sencilla simplemente copia run.sh, pppwn, stage1.bin y stage2.bin a /root del modem
- Usa los comandos de install.sh para añadir 2 líneas de comando en /etc/rc.local
- reinicia el modem si no se reinicia automáticamente

Testeado en mini router GL-MT300N-V2 Mango

Script adaptado de https://github.com/stooged/PI-Pwn

pppwn_cpp de https://github.com/xfangfang/PPPwn_cpp
