This activation method works for devices with the OpenWrt Linux system as long as they can run PPPwn C++. Check the repository of [Xfangfang](https://github.com/xfangfang/PPPwn_cpp) for compatibility.

## Requirements:

- Supports PS4 FW 9.00, 9.50, 9.51, 9.60, 10.00, 10.01 and 11.00
- Router/Modem with LAN connection and OpenWrt.
- PuTTY installed on your PC to access the terminal.
- Verify `PPPwn_cpp` for OpenWrt Linux distributions by using the command `uname -m`. It is recommended to install the MIPSEL build.
- Download `goldhen.bin` for your console's firmware from [Sistro](https://github.com/GoldHEN/GoldHEN/releases).
- USB drive with 1GB or more of storage.
- Tested model [GL-MT300N-V2 Mango](https://www.gl-inet.com/products/gl-mt300n-v2/)

## Direct Installation (Use this alternative if your router does not have enough memory space)

1. Update the mini-router system before proceeding.
2. The router device must be connected to the Internet before proceeding, as it needs to download the repository files from the terminal.
3. Run PuTTY or Git Bash and open the terminal using the router credentials.
4. From the terminal, run these commands:
    ```sh
    wget -O /tmp/installer-d.sh https://raw.githubusercontent.com/CodeInvers3/PPPwn_ow/main/installer-d.sh
    chmod +x /tmp/installer-d.sh
    /tmp/installer-d.sh
    ```
    In the end, press Enter to complete the installation.
5. Follow step 6 of the common installation.

## Common Installation 

1. Update the mini-router system before proceeding.
2. The router device must be connected to the Internet before proceeding, as it needs to download the pppwn_ow.zip package from the terminal.
3. Run PuTTY or Git Bash and open the terminal using the router credentials.
4. Check if you have `unzip` installed with the command:
    ```sh
    opkg list-installed | grep unzip
    ```
    If `command not found` appears, you must install it with the following command:
    ```sh
    opkg update
    opkg install unzip
    ```
5. From the terminal, run these commands:
    ```sh
    wget -O /tmp/installer.sh https://raw.githubusercontent.com/CodeInvers3/PPPwn_ow/main/installer.sh
    chmod +x /tmp/installer.sh
    /tmp/installer.sh
    ```
    In the end, press Enter to complete the installation.
6. Copy `goldhen.bin` to your USB drive. Make sure it is formatted in exFAT or FAT32 and connect it to your console.
7. From your PS4 console, set up a PPPoE network connection using `ppp` as the username and password.
8. Wait a few seconds until the Internet connection is established, and from the console's web browser, go to `http://<router_ip>/pppwn.html`.
9. Select the build compatible with your router device and click on "Install". Wait until the installation is complete.
10. If there is an error or you do not get the expected result on Ethernet, you can restart the installation by clicking on "Update".
11. Router models with a change button can use it to boot PPPwn.

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

## Instalación directa (Usa esta alternativa si tu router no tiene mucho espacio en la memoria)

1. Actualiza el sistema del mini-router antes de continuar.
2. El dispositivo router debe estar conectado a Internet antes de continuar, ya que requiere descargar los archivos del repositorio desde el terminal.
3. Ejecuta PuTTY o Git Bash y abre el terminal usando las credenciales del router.
4. Desde el terminal, ejecuta estos comandos:
    ```sh
    wget -O /tmp/installer-l.sh https://raw.githubusercontent.com/CodeInvers3/PPPwn_ow/main/installer-l.sh
    chmod +x /tmp/installer-l.sh
    /tmp/installer-l.sh
    ```
    Al final, presiona Enter para completar la instalación.
5. Sigue el paso 6 de la instalación normal.

## Instalación normal

1. Actualiza el sistema del mini-router antes de continuar.
2. El dispositivo router debe estar conectado a Internet antes de continuar, ya que requiere descargar el paquete pppwn_ow.zip desde el terminal.
3. Ejecuta PuTTY o Git Bash y abre el terminal usando las credenciales del router.
4. Verifica si tienes instalado `unzip` con el comando:
    ```sh
    opkg list-installed | grep unzip
    ```
    Si aparece `command not found`, debes instalarlo con el siguiente comando:
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
    Al final, presiona Enter para completar la instalación.
6. Copia `goldhen.bin` a tu memoria USB. Asegúrate de que esté formateada en exFAT o FAT32 y conéctala a tu consola.
7. Desde tu consola PS4, configura una conexión de red en PPPoE usando `ppp` como usuario y contraseña.
8. Espera unos segundos hasta que se establezca la conexión a Internet y, desde el navegador web de la consola, accede a la dirección `http://<router_ip>/pppwn.html`.
9. Selecciona la compilación compatible con tu dispositivo router y haz clic en "Instalar". Espera hasta que se complete la instalación.
10. En caso de que haya un error o no obtengas el resultado esperado en Ethernet, puedes reiniciar la instalación haciendo clic en "Update".
11. Los modelos de routers que dispongan de un botón de cambio pueden usarlo para arrancar PPPwn.

Probado en mini router [GL-MT300N-V2 Mango](https://www.gl-inet.com/products/gl-mt300n-v2/)
