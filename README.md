# PPPwn_OpenWrt
Interfaz web para arrancar PPPwn_cpp desde un navegador web.
Algunos modelos de PS4 no son vulnerables al método pppwn revisa si el tuyo lo es.
Descarga la ultima version [descargar pppwn_cpp repositorio oficial](https://nightly.link/xfangfang/PPPwn_cpp/workflows/ci.yaml/main).

## Requerimientos:

- Router/Modem conexión lan con OpenWrt.
- Tener instalado PuTTY en tu PC para acceder por el terminal.
- Descargar stage1.bin y stage2.bin desde el repositorio de [Sistro](https://github.com/SiSTR0/PPPwn/releases) para el firmware correspondiente.
- Descargar PPPwn_cpp para distribuciones Linux con chip MIPS o el que tu dispositivo tenga, verificar con el comando `uname -m`.
- Descargar goldhen.bin para el Firmware de tu consola.

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
    wget https://github.com/CodeInvers3/PPPwn_ow/archive/refs/heads/main.zip
    unzip main.zip
    chmod +x PPPwn_ow-main/install.sh
    ./PPPwn_ow-main/install.sh
    ```
    Al final, presiona Enter para completar la instalación.

3. Desde tu navegador, accede a la interfaz web creada en `http://<router_ip>/pppwn.html`.
4. Selecciona la compilación compatible con tu dispositivo router y haz clic en "Instalar". Espera hasta que se complete la instalación.
5. En caso de que haya un error o no obtengas el resultado esperado en Ethernet, puedes reiniciar la instalación haciendo clic en "Update".
6. Copia `goldhen.bin` a tu memoria USB. Asegúrate de que esté formateada en exFAT o FAT32.
7. Conecta todo a la consola PS4 y, desde el navegador, ingresa la dirección IP de tu router.


Probado en mini router [GL-MT300N-V2 Mango](https://www.gl-inet.com/products/gl-mt300n-v2/)

It enables auto-start on a Wi-Fi device running the OpenWrt system.

## Requirements:

- Smart Router lan with OpenWrt.
- Have PuTTY installed on your PC to access the terminal.
- Download stage1.bin and stage2.bin from Sistro [repository](https://github.com/SiSTR0/PPPwn/releases) for the corresponding firmware.
- Download PPPwn_cpp for Linux distributions with MIPS chip or whichever your device has, verify with the command `uname -m`.
- Download goldhen.bin for you PS4 FW

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
    wget https://github.com/CodeInvers3/PPPwn_ow/archive/refs/heads/main.zip
    unzip main.zip
    chmod +x PPPwn_ow-main/install.sh
    ./PPPwn_ow-main/install.sh
    ```
    At the end, press Enter to complete the installation.
3. From your browser, go to the web interface created at `http://<router_ip>/pppwn.html`.
4. Select the build compatible with your router device and click "Install". Wait until the installation is complete.
5. If there is an error or you do not get the expected result on Ethernet, you can restart the installation by clicking "Update".
6. Copy `goldhen.bin` to your USB drive. Make sure it is formatted in exFAT or FAT32.
7. Connect everything to the PS4 console and, from the browser, go to the IP address of your router.


Every time you turn on the router and connect the USB memory with goldhen.bin, the run.sh script will execute the pppwn command, which will allow the auto-exploit.

PPPwn from https://github.com/xfangfang/PPPwn_cpp

### Credits: TheFlowTheOfficialFloW / Sistro / Xfangfang
