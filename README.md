# PPPwn_OpenWrt
He añadido una interfaz web para arrancar PPPwn_cpp desde un teléfono solamente conectandote al router.
Descarga la ultima version [descargar pppwn_cpp repositorio oficial](https://nightly.link/xfangfang/PPPwn_cpp/workflows/ci.yaml/main).

## Requerimientos:

- Router/Modem conexión lan con OpenWrt.
- Tener instalado PuTTY en tu PC para acceder por el terminal.
- Descargar stage1.bin y stage2.bin desde el repositorio de Stooged para el firmware correspondiente.
- Descargar PPPwn_cpp para distribuciones Linux con chip MIPS o el que tu dispositivo tenga, verificar con el comando `uname -m`.
- Descargar goldhen.bin para el Firmware de tu consola.

## Instalación

1. Desde el terminal en su router ejecutan el comando `cd ` y depues `wget https://github.com/CodeInvers3/PPPwn_ow/archive/refs/heads/main.zip`
2. Despues ejecutar el comando `unzip main` y por ultimo el comando `PPPwn_ow-main/install.sh`

## Pasos para el procedimiento:

1. Conectar tu dispositivo a la PC mediante el cable LAN.
2. Configurar el nombre de usuario y contraseña. Si lo requieres, puedes configurar una conexión Wi-Fi en tu dispositivo.
3. Acceder desde el terminal con PuTTY utilizando el comando `ssh usuario@ip_del_router`.
4. Descargar y copiar los archivos run.sh, install.sh, pppwn, stage1.bin y stage2.bin al directorio /root en tu dispositivo con el comando `cp /mnt/usb/* /root`. Esto puedes hacerlo desde tu memoria USB conectándola al dispositivo.
5. Copiar goldhen.bin a la memoria USB.
6. Ejecutar install.sh o las líneas de comando contenidas en install.sh.
7. Reiniciar el dispositivo.
8. Conectar la memoria USB con golden.bin a la consola PS4.
  
Cada vez que enciendas el router y conectes la memoria USB con goldhen.bin, el script run.sh ejecutará el comando pppwn, lo que permitirá el autoexploit.

Probado en mini router GL-MT300N-V2 Mango

This is an adaptation of Stooged’s script to work with PPPwn_cpp.

It enables auto-start on a Wi-Fi device running the OpenWrt system.

## Requirements:

- Smart Router lan with OpenWrt.
- Have PuTTY installed on your PC to access the terminal.
- Download stage1.bin and stage2.bin from Stooged’s repository for the corresponding firmware.
- Download PPPwn_cpp for Linux distributions with MIPS chip or whichever your device has, verify with the command `uname -m`.
- Download goldhen.bin for you PS4 FW

## Steps for the procedure:

1. Connect your device to the PC using a LAN cable.
2. Set up the username and password. If required, you can configure a Wi-Fi connection on your device.
3. Access from the terminal with PuTTY using the command `ssh username@router_ip`.
4. Download and copy the files run.sh, install.sh, pppwn, stage1.bin, and stage2.bin to the /root directory on your device with the command `cp /mnt/usb/* /root`. You can do this from your USB memory by connecting it to the device.
5. Copy goldhen.bin in your USB memory.
6. Execute install.sh or the command lines contained in install.sh.
7. Restart the device.
8. Connect the USB memory stick with golden.bin to the PS4 console.

Every time you turn on the router and connect the USB memory with goldhen.bin, the run.sh script will execute the pppwn command, which will allow the auto-exploit.

PPPwn from https://github.com/xfangfang/PPPwn_cpp

### Credits: Stooged / Xfangfang
