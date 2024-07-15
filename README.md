Minimal version

## Features

- Supports PS4 FW 9.00, 9.50, 9.51, 9.60, 10.00, 10.01 and 11.00
- Required minimal memory flash space
- Tested model [GL-MT300N-V2 Mango](https://www.gl-inet.com/products/gl-mt300n-v2/)

## Tools
- Router/Modem with LAN connection and OpenWrt.
- PuTTY installed on your PC to access the terminal.
- Verify `PPPwn_cpp` for OpenWrt Linux distributions by using the command `uname -m`. It is recommended to install the MIPSEL build.
- Download WinSCP from [WinSCP Windows](https://winscp.net/eng/index.php)
- Download pppwn from [Repository xfangfang/PPPwn_cpp](https://nightly.link/xfangfang/PPPwn_cpp/workflows/ci.yaml/main?status=completed)
- Download `goldhen.bin` for your console's firmware from [Sistro](https://github.com/GoldHEN/GoldHEN/releases).
- USB drive with 1GB or more of storage.

## Installation

1. Install OpenWrt on the device.
2. Create Credentials user and password.
4. Using WinSCP, transfer the directories `stage1` and `stage2` to `/root/`
5. Transfer the files `run.sh` and `pw.conf` to `/root/`
6. Transfer `wps` to `/etc/rc.button/` and transfer the `pppwn` executable to `/usr/bin/`
7. Run PuTTY or Git Bash and open the terminal using the router credentials.
8. From the terminal, run these commands:
    ```sh
    sed -i '/exit 0/d' /etc/rc.local
    echo '/root/run.sh &' >> /etc/rc.local
    echo 'exit 0' >> /etc/rc.local
    chmod +x /root/run.sh
    chmod +x /etc/rc.button/wps
    chmod +x /usr/bin/pppwn
    ```
    This enabled autorun when turn on device and enable the reset/WPS button on TP-Link routers.
9. Modify pw.conf to change the firmware version to version=XXXX
10. Use Button reset o WPS to execute pppwn.
