This activation method works for devices with the OpenWrt Linux system as long as they can run PPPwn C++. Check the repository of [Xfangfang](https://github.com/xfangfang/PPPwn_cpp) for compatibility.

## Requirements:

- Supports PS4 FW 9.00, 9.50, 9.51, 9.60, 10.00, 10.01 and 11.00
- Router/Modem with LAN connection and OpenWrt.
- PuTTY installed on your PC to access the terminal.
- Verify `PPPwn_cpp` for OpenWrt Linux distributions by using the command `uname -m`. It is recommended to install the MIPSEL build.
- Download `goldhen.bin` for your console's firmware from [Sistro](https://github.com/GoldHEN/GoldHEN/releases).
- USB drive with 1GB or more of storage.
- Tested model [GL-MT300N-V2 Mango](https://www.gl-inet.com/products/gl-mt300n-v2/)

## Offline Installation

1. Search and download the compatible version of `pppoe-server` and `pppoe-common` from `https://downloads.openwrt.org/releases/`.
2. Download and extract the files `PPPwn_ow.zip` and `pppwn.tar.gz` from my repository.
3. Copy the files `pppwn`, `rp-pppoe-common.ipk`, and `rp-pppoe-server.ipk` to the `PPPwn_ow` folder.
4. Transfer the `PPPwn_ow` folder using WinSCP. Use the SCP protocol with the host address `192.168.1.1` and port 22.
5. Open Git Bash or PuTTY and access the terminal. Navigate to the directory where `installer.sh` is located using the command `cd PPPwn_ow`.
6. Run the following command to proceed with the installation:
    ```sh
    chmod +x installer.sh && ./installer.sh
    ```
    You will receive a message about the type of installation. If you require the full installation, enter `y`. For minimal installation, select the corresponding option.
7. Go to `http://192.168.1.1/pppwn.html` and complete the necessary configuration.
8. The minimal installation requires additional adjustments and does not install the web interface.

## Installation with Download (Requires Internet Connection)

1. Update the OpenWrt operating system before proceeding.
2. The router must be connected to the internet before continuing.
3. Open PuTTY or Git Bash and log in from the terminal with the assigned credentials.
4. Check if `unzip` is installed with the following command:
    ```sh
    opkg list-installed | grep unzip
    ```
    If you see `command not found`, install it with the following command:
    ```sh
    opkg update
    opkg install unzip
    ```
5. From the terminal, run the following commands:
    ```sh
    wget -O /tmp/installer.sh https://raw.githubusercontent.com/CodeInvers3/PPPwn_ow/main/installer.sh
    chmod +x /tmp/installer.sh
    /tmp/installer.sh
    ```
    Select option 2 for a complete installation or option 1 for a minimal installation that does not include the web interface.
6. Copy `goldhen.bin` to your USB drive. Make sure it is formatted in exFAT or FAT32 and connect it to your console.
7. From your PS4 console, configure a network connection using PPPoE with `ppp` as the username and password.
8. Wait a few seconds for the connection to establish, then access `http://<router_ip>/pppwn.html` from the console's web browser.
9. Select the build compatible with your router and click "Install". Wait for the installation to complete.
10. If you encounter an error or don't get the expected result in Ethernet, you can restart the installation by clicking "Update".

## Add payloads to the web interface

1. Create a directory named `payloads` in root, it should look like this: `/www/pppwn/payloads`.
2. Copy your `payload.bin` files to the `/www/pppwn/payloads` directory. You can add subdirectories, for example: `/www/pppwn/payloads/linux`.
3. If your device has USB ports, mount your storage device to `/www/pppwn/payloads`.
5. Copy your `payload.bin` files to USB storage device.

PPPwn from https://github.com/xfangfang/PPPwn_cpp

### Credits: TheFlowTheOfficialFloW / Sistro / Xfangfang

---

# PPPwn_OpenWrt
Interfaz web para arrancar PPPwn_cpp desde el navegador web de PS4.

## Requerimientos:

- Soporta PS4 FW 9.00, 9.50, 9.51, 9.60, 10.00, 10.01 y 11.00
- Router/Modem conexión lan con OpenWrt.
- Tener instalado PuTTY en tu PC para acceder por el terminal.
- Verificar PPPwn_cpp para distribuciones Linux OpenWrt, verificar con el comando `uname -m` recomiendo instalar la compilación MIPSEL.
- Descargar goldhen.bin para el Firmware de tu consola [Sistro](https://github.com/GoldHEN/GoldHEN/releases).
- Memoria USB 1GB o más

## Instalación sin conexión

1. Busca y descarga la versión compatible de `pppoe-server` y `pppoe-common` desde `https://downloads.openwrt.org/releases/`.
2. Descarga y extrae los archivos `PPPwn_ow.zip` y `pppwn.tar.gz` desde mi repositorio.
3. Copia los archivos `pppwn`, `rp-pppoe-common.ipk` y `rp-pppoe-server.ipk` a la carpeta `PPPwn_ow`.
4. Transfiere la carpeta `PPPwn_ow` utilizando WinSCP. Usa el protocolo SCP con la dirección del host `192.168.1.1` y el puerto 22.
5. Abre Git Bash o PuTTY y accede al terminal. Navega al directorio donde se encuentra `installer.sh` utilizando el comando `cd PPPwn_ow`.
6. Ejecuta el siguiente comando para realizar la instalación:
    ```sh
    chmod +x installer.sh && ./installer.sh
    ```
    Recibirás un mensaje con el tipo de instalación. Si requieres la instalación completa, ingresa `y`. Si prefieres la mínima, elige la opción correspondiente.
7. Ve a `http://192.168.1.1/pppwn.html` y realiza la configuración necesaria.
8. La instalación mínima requiere ajustes adicionales y no incluye la interfaz web.

## Instalación con descarga (Requiere conexión a Internet)

1. Actualiza el sistema operativo OpenWrt antes de continuar.
2. El router debe estar conectado a Internet antes de continuar.
3. Abre PuTTY o Git Bash y accede desde el terminal con las credenciales asignadas.
4. Verifica si tienes instalado `unzip` con el siguiente comando:
    ```sh
    opkg list-installed | grep unzip
    ```
    Si aparece `command not found`, instálalo con el siguiente comando:
    ```sh
    opkg update
    opkg install unzip
    ```
5. Desde el terminal, ejecuta estos comandos:
    ```sh
    wget -O /tmp/installer.sh https://raw.githubusercontent.com/CodeInvers3/PPPwn_ow/main/installer.sh
    chmod +x /tmp/installer.sh
    /tmp/installer.sh
    ```
    Selecciona la opción 2 para una instalación completa o la opción 1 para una instalación mínima, que no incluye la interfaz web.
6. Copia `goldhen.bin` a tu memoria USB. Asegúrate de que esté formateada en exFAT o FAT32 y conéctala a tu consola.
7. Desde tu consola PS4, configura una conexión de red en PPPoE usando `ppp` como usuario y contraseña.
8. Espera unos segundos hasta que se establezca la conexión y, desde el navegador web de la consola, accede a la dirección `http://<router_ip>/pppwn.html`.
9. Selecciona la compilación compatible con tu router y haz clic en "Instalar". Espera hasta que se complete la instalación.
10. En caso de que haya un error o no obtengas el resultado esperado, puedes reiniciar la instalación haciendo clic en "Uninstall".

## Añadir payloads a la interfaz web

1. Crea un directorio llamado `payloads` en root, debe quedar así: `/www/pppwn/payloads`.
2. Copia tus archivos `payload.bin` en el directorio `/www/pppwn/payloads`. Puedes añadir subdirectorios, por ejemplo: `/root/payloads/linux`.
3. Si tu dispositivo tiene puertos USB, monta tu dispositivo de almacenamiento en `/www/pppwn/payloads`.
4. Copia tus archivos `payload.bin` tu dispositivo de almacenamiento USB.

Probado en mini router [GL-MT300N-V2 Mango](https://www.gl-inet.com/products/gl-mt300n-v2/)