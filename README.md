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
2. The router device must be connected to the Internet before proceeding, as it needs to download the repository files from the terminal.
3. Run PuTTY or Git Bash and open the terminal using the router credentials.
4. Using WinSCP, transfer the directories stage1 and stage2 to /root/, transfer run.sh to /root/, transfer wps to /etc/rc.button/ and transfer the pppwn executable to /usr/bin/
5. From the terminal, run these commands:
    ```sh
    sed -i '/exit 0/d' /etc/rc.local
    echo '/root/run.sh &' >> /etc/rc.local
    echo 'exit 0' >> /etc/rc.local
    chmod +x /root/run.sh
    chmod +x /etc/rc.button/wps
    ```
    This enabled autorun when turn on device and enable the reset/WPS button on TP-Link routers.
6. Modify pw.conf to change the firmware version to version=XXXX
7. Use Button reset o WPS to execute pppwn.
