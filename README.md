# PPPwn_OpenWrt
Interfaz web para arrancar PPPwn_cpp desde un navegador web.
Algunos modelos de PS4 no son vulnerables al método pppwn revisa si el tuyo lo es.

## Requerimientos:

- Soporta PS4 FW 9.00, 10.00, 10.01 y 11.00
- Router/Modem conexión lan con OpenWrt.
- Tener instalado PuTTY en tu PC para acceder por el terminal.
- Verificar PPPwn_cpp para distribuciones Linux OpenWrt, verificar con el comando `uname -m` recomiendo instalar la compilación MIPSEL.
- Descargar goldhen.bin para el Firmware de tu consola [Sistro](https://github.com/GoldHEN/GoldHEN/releases).
- Memoria USB 1GB o más

## Instalación

1. Verifica si tienes instalado `unzip`:
    ```sh
    opkg list-installed | grep unzip
    ```
    Si no está instalado, instala `unzip` con el siguiente comando:
    ```sh
    opkg update
    opkg install unzip
    ```
2. Desde el terminal en tu router, ejecuta estos comandos:
    ```sh
    cd
    wget -O main.zip https://github.com/CodeInvers3/PPPwn_ow/archive/refs/heads/main.zip
    unzip main.zip -d /tmp
    chmod +x /tmp/PPPwn_ow-main/install.sh
    /tmp/PPPwn_ow-main/install.sh
    ```
    Al final, presiona Enter para completar la instalación.
3. Copia `goldhen.bin` a tu memoria USB. Asegúrate de que esté formateada en exFAT o FAT32 y conéctala a tu consola.
4. Desde tu consola PS4, configura una conexión de red en PPPoE usando `ppp` como usuario y contraseña.
5. Espera unos segundos hasta que se establezca la conexión a internet y, desde el navegador web de la consola, accede a la dirección `http://<router_ip>/pppwn.html`.
6. Selecciona la compilación compatible con tu dispositivo router y haz clic en "Instalar". Espera hasta que se complete la instalación.
7. En caso de que haya un error o no obtengas el resultado esperado en Ethernet, puedes reiniciar la instalación haciendo clic en "Update".


Probado en mini router [GL-MT300N-V2 Mango](https://www.gl-inet.com/products/gl-mt300n-v2/)

---

This activation method works for devices with the OpenWrt Linux system as long as they can run PPPwn C++. Check the repository of [Xfangfang](https://github.com/xfangfang/PPPwn_cpp) for compatibility.

## Requirements:

- Supports PS4 FW 9.00, 10.00, 10.01 and 11.00
- Router/Modem with LAN connection and OpenWrt.
- PuTTY installed on your PC to access the terminal.
- Verify `PPPwn_cpp` for OpenWrt Linux distributions by using the command `uname -m`. It is recommended to install the MIPSEL build.
- Download `goldhen.bin` for your console's firmware from [Sistro](https://github.com/GoldHEN/GoldHEN/releases).
- USB drive with 1GB or more of storage.

## Steps installation:

1. Check if `unzip` is installed:
    ```sh
    opkg list-installed | grep unzip
    ```
    If it is not installed, install `unzip` with the following command:
    ```sh
    opkg update
    opkg install unzip
    ```
2. From the terminal on your router, run these commands:
    ```sh
    cd
    wget -O main.zip https://github.com/CodeInvers3/PPPwn_ow/archive/refs/heads/main.zip
    unzip main.zip -d /tmp
    chmod +x /tmp/PPPwn_ow-main/install.sh
    /tmp/PPPwn_ow-main/install.sh
    ```
    At the end, press Enter to complete the installation.
3. Copy `goldhen.bin` to your USB drive. Make sure it is formatted in exFAT or FAT32 and connect it to your console.
4. From your PS4 console, set up a PPPoE network connection using `ppp` as the username and password.
5. Wait a few seconds until the internet connection is established and, from the console's web browser, go to `http://<router_ip>/pppwn.html`.
6. Select the build compatible with your router device and click "Install". Wait until the installation is complete.
7. In case there is an error or you do not get the expected result on Ethernet, you can restart the installation by clicking "Update".


Every time you turn on the router and connect the USB memory with goldhen.bin, the run.sh script will execute the pppwn command, which will allow the auto-exploit.

PPPwn from https://github.com/xfangfang/PPPwn_cpp

### Credits: TheFlowTheOfficialFloW / Sistro / Xfangfang
