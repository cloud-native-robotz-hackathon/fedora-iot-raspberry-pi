# fedora-iot-raspberry-pi

## Work-in-progress, right now it's not clear if it will work

This is our Fedora IoT for Raspberry pi 4 with an Dexter GoPiGo3 board

## Hardware informations:

* https://github.com/DexterInd/GoPiGo3/blob/master/Hardware/GoPiGo3%20v3.2.0.pdf

## Research

- Issue from @goetzrieger to run GoPiGo3 on non-Debian: https://github.com/DexterInd/GoPiGo3/issues/320
- API Spec: https://gopigo3.readthedocs.io/en/master/api-basic/easygopigo3.html#easygopigo3.EasyGoPiGo3.backward
- python behind: https://github.com/DexterInd/GoPiGo3/blob/master/Software/Python/gopigo3.py#L33
  - It use move the robots it use spidev: https://pypi.org/project/spidev/
  - pigpio is only used to set some settings: https://github.com/DexterInd/GoPiGo3/blob/b50cfce3eced2b8d97132b1eef58cd3606ec1025/Software/Python/gopigo3.py#L231-L235
- Hardware Port description: 
   - https://gopigo3.readthedocs.io/en/master/api-basic/structure.html#hardware-ports 
   - https://gopigo3.readthedocs.io/en/master/quickstart.html#getting-familiar-with-the-gopigo3  
- Containerized pigpiod: https://hub.docker.com/r/zinen2/alpine-pigpiod
- pigiod in generall: https://abyz.me.uk/rpi/pigpio/pigpiod.html

Infos about new GPIO user space interface: https://sergioprado.blog/new-linux-kernel-gpio-user-space-interface/ 

## /dev/gpiomem - not available

Looks like this is a kernel module:

https://github.com/raspberrypi/linux/blob/9da8d6df2051478f0ba16d73c65995955c19cb3a/arch/arm/configs/bcm2711_defconfig#L705

```
root@t-1000:~# lsmod | grep gpio
bcm2835_gpiomem        16384  2
root@t-1000:~#
```

Let's ignore it and use /dev/mem

## GPIO Setup

https://github.com/DexterInd/GoPiGo3/blob/master/Software/Python/gopigo3.py#L231-L235

```pythyon
        # Make sure the SPI lines are configured for mode ALT0 so that the hardware SPI controller can use them
        # subprocess.call('gpio mode 12 ALT0', shell=True)
        # subprocess.call('gpio mode 13 ALT0', shell=True)
        # subprocess.call('gpio mode 14 ALT0', shell=True)
        import pigpio
        pi_gpio = pigpio.pi()
        pi_gpio.set_mode(9, pigpio.ALT0)
        pi_gpio.set_mode(10, pigpio.ALT0)
        pi_gpio.set_mode(11, pigpio.ALT0)
        pi_gpio.stop()
```

<details>
<summary>Get & Set GPIO lines via memory</summary>

#### Robocop (Fedora)

```shell
./set-line-mode.py
GPIO 07 set to Output
GPIO 08 set to Output
GPIO 23 set to Output
GPIO 09 set to ALT0 (PWM0)
GPIO 10 set to ALT0 (PWM0)
GPIO 11 set to ALT0 (PWM0)
./get-line-mode.py
GPIO 00 Mode: Input
GPIO 01 Mode: Input
GPIO 02 Mode: Alt0
GPIO 03 Mode: Alt0
GPIO 04 Mode: Input
GPIO 05 Mode: Input
GPIO 06 Mode: Input
GPIO 07 Mode: Output
GPIO 08 Mode: Output
GPIO 09 Mode: Alt0
GPIO 10 Mode: Alt0
GPIO 11 Mode: Alt0
GPIO 12 Mode: Input
GPIO 13 Mode: Input
GPIO 14 Mode: Alt5
GPIO 15 Mode: Alt5
GPIO 16 Mode: Input
GPIO 17 Mode: Input
GPIO 18 Mode: Input
GPIO 19 Mode: Input
GPIO 20 Mode: Input
GPIO 21 Mode: Input
GPIO 22 Mode: Input
GPIO 23 Mode: Output
GPIO 24 Mode: Input
GPIO 25 Mode: Input
GPIO 26 Mode: Input
GPIO 27 Mode: Input
GPIO 28 Mode: Alt5
GPIO 29 Mode: Alt5
GPIO 30 Mode: Alt3
GPIO 31 Mode: Alt3
GPIO 32 Mode: Alt3
GPIO 33 Mode: Alt3
GPIO 34 Mode: Alt3
GPIO 35 Mode: Alt3
GPIO 36 Mode: Alt3
GPIO 37 Mode: Alt3
GPIO 38 Mode: Alt3
GPIO 39 Mode: Alt3
GPIO 40 Mode: Alt0
GPIO 41 Mode: Alt0
GPIO 42 Mode: Output
GPIO 43 Mode: Input
GPIO 44 Mode: Input
GPIO 45 Mode: Input
GPIO 46 Mode: Input
GPIO 47 Mode: Input
GPIO 48 Mode: Input
GPIO 49 Mode: Input
GPIO 50 Mode: Input
GPIO 51 Mode: Input
GPIO 52 Mode: Input
```

#### T-1000 (Rasbian)

```shell
root@t-1000:~/edgecontroller# python3 ./get-line-mode.py
GPIO 00 Mode: Input
GPIO 01 Mode: Input
GPIO 02 Mode: Alt0
GPIO 03 Mode: Alt0
GPIO 04 Mode: Input
GPIO 05 Mode: Input
GPIO 06 Mode: Input
GPIO 07 Mode: Output
GPIO 08 Mode: Output
GPIO 09 Mode: Alt0
GPIO 10 Mode: Alt0
GPIO 11 Mode: Alt0
GPIO 12 Mode: Input
GPIO 13 Mode: Input
GPIO 14 Mode: Alt5
GPIO 15 Mode: Alt5
GPIO 16 Mode: Input
GPIO 17 Mode: Input
GPIO 18 Mode: Input
GPIO 19 Mode: Input
GPIO 20 Mode: Input
GPIO 21 Mode: Input
GPIO 22 Mode: Input
GPIO 23 Mode: Output
GPIO 24 Mode: Input
GPIO 25 Mode: Input
GPIO 26 Mode: Input
GPIO 27 Mode: Input
GPIO 28 Mode: Alt5
GPIO 29 Mode: Alt5
GPIO 30 Mode: Alt3
GPIO 31 Mode: Alt3
GPIO 32 Mode: Alt3
GPIO 33 Mode: Alt3
GPIO 34 Mode: Alt3
GPIO 35 Mode: Alt3
GPIO 36 Mode: Alt3
GPIO 37 Mode: Alt3
GPIO 38 Mode: Alt3
GPIO 39 Mode: Alt3
GPIO 40 Mode: Alt0
GPIO 41 Mode: Alt0
GPIO 42 Mode: Output
GPIO 43 Mode: Input
GPIO 44 Mode: Input
GPIO 45 Mode: Input
GPIO 46 Mode: Input
GPIO 47 Mode: Input
GPIO 48 Mode: Input
GPIO 49 Mode: Input
GPIO 50 Mode: Input
GPIO 51 Mode: Input
GPIO 52 Mode: Input
```

</details>








## Important Hardware access

- [ ] Camera access
- [ ] Distance sensor access
- [ ] Control the motors (via SPI)

## Scrabble

### Started with an Fedora Workstation installation



### Enable `iomem=relaxed` (add to boot parameter)

TBD

Import for `get-line-mode.py` and `set-line-mode.py`

### How to get /dev/spidev0.1


SPI device is disabled:

```shell

root@robocop:~# ls -lda /sys/firmware/devicetree/base/soc/spi@7e2*
drwxr-xr-x. 2 root root 0 Mar 18 15:47 /sys/firmware/devicetree/base/soc/spi@7e204000
drwxr-xr-x. 2 root root 0 Mar 18 15:47 /sys/firmware/devicetree/base/soc/spi@7e204600
drwxr-xr-x. 2 root root 0 Mar 18 15:47 /sys/firmware/devicetree/base/soc/spi@7e204800
drwxr-xr-x. 2 root root 0 Mar 18 15:47 /sys/firmware/devicetree/base/soc/spi@7e204a00
drwxr-xr-x. 2 root root 0 Mar 18 15:47 /sys/firmware/devicetree/base/soc/spi@7e204c00
drwxr-xr-x. 2 root root 0 Mar 18 15:47 /sys/firmware/devicetree/base/soc/spi@7e215080
drwxr-xr-x. 2 root root 0 Mar 18 15:47 /sys/firmware/devicetree/base/soc/spi@7e2150c0
root@robocop:~# cat /sys/firmware/devicetree/base/soc/spi@7e204000/status
disabledroot@robocop:~#
root@robocop:~# cat /sys/firmware/devicetree/base/soc/spi@7e204000/status ; echo
disabled
root@robocop:~# cat /sys/firmware/devicetree/base/soc/spi@7e204000/status ; echo
disabled
root@robocop:~#



root@t-1000:/boot# ls -lda /sys/firmware/devicetree/base/soc/spi@7e2*
drwxr-xr-x 4 root root 0 Mar 18 19:45 /sys/firmware/devicetree/base/soc/spi@7e204000
drwxr-xr-x 2 root root 0 Mar 18 19:45 /sys/firmware/devicetree/base/soc/spi@7e204600
drwxr-xr-x 2 root root 0 Mar 18 19:45 /sys/firmware/devicetree/base/soc/spi@7e204800
drwxr-xr-x 2 root root 0 Mar 18 19:45 /sys/firmware/devicetree/base/soc/spi@7e204a00
drwxr-xr-x 2 root root 0 Mar 18 19:45 /sys/firmware/devicetree/base/soc/spi@7e204c00
drwxr-xr-x 2 root root 0 Mar 18 19:45 /sys/firmware/devicetree/base/soc/spi@7e215080
drwxr-xr-x 2 root root 0 Mar 18 19:45 /sys/firmware/devicetree/base/soc/spi@7e2150c0
root@t-1000:/boot# cat /sys/firmware/devicetree/base/soc/spi@7e204000/status ; echo
okay
root@t-1000:/boot#

```

=> force enable it:

```shell
fdtput --type s /boot/dtb/broadcom/bcm2711-rpi-4-b.dtb /soc/spi@7e204000 status "okay"
```

=> dmesg
```
[    2.916265] spi-bcm2835 fe204000.spi: error -ENODEV: no tx-dma configuration found - not using dma mode
```



Looks like the raspberry pi kernel/device tree is prepared for the device.

Dump device tree the the robotos:
```
dtc -I fs /proc/device-tree > /tmp/t-1000.dtdump
```

Let's compare `spi@7e204000`

Robot with Fedora:
```shell
cat robocop.dtdump | grep -i 'spi@7e204000 {' -A35
                spi@7e204000 {
                        #address-cells = <0x01>;
                        interrupts = <0x00 0x76 0x04>;
                        clocks = <0x07 0x14>;
                        #size-cells = <0x00>;
                        compatible = "brcm,bcm2835-spi";
                        status = "okay";
                        reg = <0x7e204000 0x200>;
                        phandle = <0x81>;
                };

                dpi@7e208000 {
                        clock-names = "core", "pixel";
```

Robot with Rasbian
```shell
cat t-1000.dtdump | grep -i 'spi@7e204000 {' -A35
                spi@7e204000 {
                        pinctrl-names = "default";
                        #address-cells = <0x01>;
                        pinctrl-0 = <0x0e 0x0f>;
                        interrupts = <0x00 0x76 0x04>;
                        clocks = <0x08 0x14>;
                        #size-cells = <0x00>;
                        dma-names = "tx\0rx";
                        compatible = "brcm,bcm2835-spi";
                        status = "okay";
                        reg = <0x7e204000 0x200>;
                        phandle = <0x34>;
                        dmas = <0x0c 0x06 0x0c 0x07>;
                        cs-gpios = <0x07 0x08 0x01 0x07 0x07 0x01>;

                        spidev@0 {
                                #address-cells = <0x01>;
                                #size-cells = <0x00>;
                                spi-max-frequency = <0x7735940>;
                                compatible = "spidev";
                                reg = <0x00>;
                                phandle = <0xb0>;
                        };

                        spidev@1 {
                                #address-cells = <0x01>;
                                #size-cells = <0x00>;
                                spi-max-frequency = <0x7735940>;
                                compatible = "spidev";
                                reg = <0x01>;
                                phandle = <0xb1>;
                        };
                };

                dpi@7e208000 {
                        #address-cells = <0x01>;

```

![Image](https://github.com/user-attachments/assets/718e305a-1606-4651-b761-f33e7396585f)

raspberrypi kernel: https://github.com/raspberrypi/linux/blob/rpi-5.15.y/arch/arm/boot/dts/bcm2711-rpi-4-b.dts#L326-L346

vs upstream: https://github.com/torvalds/linux/blob/master/arch/arm/boot/dts/broadcom/bcm2711-rpi-4-b.dts spidev0: spidev@0 is missing

Looks like this was a problem with Pi 3 as well: https://freeshell.de/less/post/fedorarpispi/



<details>
<summary>Let's try the kernel stuff</summary>

https://freeshell.de/less/post/fedorarpispi/

```shell
% dnf install -y rpmdevtools
% dnf builddep -y kernel
% dnf download --source kernel
% rpm -i kernel-*.src.rpm
% cd rpmbuild

root@robocop:~/rpmbuild# rpmbuild -bp SPECS/kernel.spec

setting SOURCE_DATE_EPOCH=1741824000
error: Failed build dependencies:
        opencsd-devel >= 1.0.0 is needed by kernel-6.13.7-200.fc41.aarch64


dnf install -t opencsd-devel

rpmbuild -bp SPECS/kernel.spec

cd /root/rpmbuild/BUILD/kernel-6.13.7-build/kernel-6.13.7/linux-6.13.7-200.fc41.aarch64/arch/arm/boot/dts/broadcom

 curl -L -O https://raw.githubusercontent.com/raspberrypi/linux/refs/heads/rpi-6.13.y/arch/arm/boot/dts/broadcom/bcm2711-rpi-4-b.dts
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  8909  100  8909    0     0  41676      0 --:--:-- --:--:-- --:--:-- 42023

cpp -I../../../../../include -E -P -x assembler-with-cpp bcm2711-rpi-4-b.dts | dtc -I dts -O dtb -o bcm2711-rpi-4-b.dts -


cpp -I../../../../../include -nostdinc -undef -x assembler-with-cpp \
  bcm2711-rpi-4-b.dts > preprocessed.dts


root@robocop:~/rpmbuild/BUILD/kernel-6.13.7-build/kernel-6.13.7/linux-6.13.7-200.fc41.aarch64/arch/arm/boot/dts/broadcom# cpp -I../../../../../include -E
 -P -x assembler-with-cpp bcm2711-rpi-4-b.dts | dtc -I dts -O dtb -o bcm2711-rpi-4-b.dts -
bcm2711-rpi-4-b.dts:12:10: fatal error: bcm270x.dtsi: No such file or directory
   12 | #include "bcm270x.dtsi"
      |          ^~~~~~~~~~~~~~
compilation terminated.
<stdin>:41.6-405.4: Warning (unit_address_vs_reg): /soc: node has a reg or ranges property, but no unit name
  also defined at <stdin>:446.6-777.4
  also defined at <stdin>:1473.6-1492.4
<stdin>:778.21-791.4: Warning (unit_address_vs_reg): /emmc2bus: node has a reg or ranges property, but no unit name
<stdin>:881.6-947.4: Warning (unit_address_vs_reg): /scb: node has a reg or ranges property, but no unit name
<stdin>:1474.22-1481.5: Warning (simple_bus_reg): /soc/firmware: missing or empty reg/ranges property
  also defined at <stdin>:1572.11-1583.3
<stdin>:1482.16-1486.5: Warning (simple_bus_reg): /soc/power: missing or empty reg/ranges property

 curl -L -O https://raw.githubusercontent.com/raspberrypi/linux/refs/heads/rpi-6.13.y/arch/arm/boot/dts/broadcom/bcm270x.dtsi
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  5546  100  5546    0     0  18460      0 --:--:-- --:--:-- --:--:-- 18486

cpp -I../../../../../include -E -P -x assembler-with-cpp bcm2711-rpi-4-b.dts | dtc -I dts -O dtb -o bcm2711-rpi-4-b.dtb -

A LOT of outout...

cp /boot/dtb/broadcom/bcm2711-rpi-4-b.dtb /boot/dtb/broadcom/bcm2711-rpi-4-b.dtb.ORIG

gcc -I ../../../../../include -E -nostdinc -undef -D__DTS__ -x assembler-with-cpp -o merged.dts bcm2711-rpi-4-b.dts




```

</details># fedora-iot-raspberry-pi

## Work-in-progress, right now it's not clear if it will work

This is our Fedora IoT for Raspberry pi 4 with an Dexter GoPiGo3 board

## Hardware informations:

* https://github.com/DexterInd/GoPiGo3/blob/master/Hardware/GoPiGo3%20v3.2.0.pdf

## Research

- Issue from @goetzrieger to run GoPiGo3 on non-Debian: https://github.com/DexterInd/GoPiGo3/issues/320
- API Spec: https://gopigo3.readthedocs.io/en/master/api-basic/easygopigo3.html#easygopigo3.EasyGoPiGo3.backward
- python behind: https://github.com/DexterInd/GoPiGo3/blob/master/Software/Python/gopigo3.py#L33
  - It use move the robots it use spidev: https://pypi.org/project/spidev/
  - pigpio is only used to set some settings: https://github.com/DexterInd/GoPiGo3/blob/b50cfce3eced2b8d97132b1eef58cd3606ec1025/Software/Python/gopigo3.py#L231-L235
- Hardware Port description: 
   - https://gopigo3.readthedocs.io/en/master/api-basic/structure.html#hardware-ports 
   - https://gopigo3.readthedocs.io/en/master/quickstart.html#getting-familiar-with-the-gopigo3  
- Containerized pigpiod: https://hub.docker.com/r/zinen2/alpine-pigpiod
- pigiod in generall: https://abyz.me.uk/rpi/pigpio/pigpiod.html

Infos about new GPIO user space interface: https://sergioprado.blog/new-linux-kernel-gpio-user-space-interface/ 

## GPIO Setup

https://github.com/DexterInd/GoPiGo3/blob/master/Software/Python/gopigo3.py#L231-L235

```pythyon
        # Make sure the SPI lines are configured for mode ALT0 so that the hardware SPI controller can use them
        # subprocess.call('gpio mode 12 ALT0', shell=True)
        # subprocess.call('gpio mode 13 ALT0', shell=True)
        # subprocess.call('gpio mode 14 ALT0', shell=True)
        import pigpio
        pi_gpio = pigpio.pi()
        pi_gpio.set_mode(9, pigpio.ALT0)
        pi_gpio.set_mode(10, pigpio.ALT0)
        pi_gpio.set_mode(11, pigpio.ALT0)
        pi_gpio.stop()
```

<details>
<summary>Get & Set GPIO lines via memory</summary>

#### Robocop (Fedora)

```shell
./set-line-mode.py
GPIO 07 set to Output
GPIO 08 set to Output
GPIO 23 set to Output
GPIO 09 set to ALT0 (PWM0)
GPIO 10 set to ALT0 (PWM0)
GPIO 11 set to ALT0 (PWM0)
./get-line-mode.py
GPIO 00 Mode: Input
GPIO 01 Mode: Input
GPIO 02 Mode: Alt0
GPIO 03 Mode: Alt0
GPIO 04 Mode: Input
GPIO 05 Mode: Input
GPIO 06 Mode: Input
GPIO 07 Mode: Output
GPIO 08 Mode: Output
GPIO 09 Mode: Alt0
GPIO 10 Mode: Alt0
GPIO 11 Mode: Alt0
GPIO 12 Mode: Input
GPIO 13 Mode: Input
GPIO 14 Mode: Alt5
GPIO 15 Mode: Alt5
GPIO 16 Mode: Input
GPIO 17 Mode: Input
GPIO 18 Mode: Input
GPIO 19 Mode: Input
GPIO 20 Mode: Input
GPIO 21 Mode: Input
GPIO 22 Mode: Input
GPIO 23 Mode: Output
GPIO 24 Mode: Input
GPIO 25 Mode: Input
GPIO 26 Mode: Input
GPIO 27 Mode: Input
GPIO 28 Mode: Alt5
GPIO 29 Mode: Alt5
GPIO 30 Mode: Alt3
GPIO 31 Mode: Alt3
GPIO 32 Mode: Alt3
GPIO 33 Mode: Alt3
GPIO 34 Mode: Alt3
GPIO 35 Mode: Alt3
GPIO 36 Mode: Alt3
GPIO 37 Mode: Alt3
GPIO 38 Mode: Alt3
GPIO 39 Mode: Alt3
GPIO 40 Mode: Alt0
GPIO 41 Mode: Alt0
GPIO 42 Mode: Output
GPIO 43 Mode: Input
GPIO 44 Mode: Input
GPIO 45 Mode: Input
GPIO 46 Mode: Input
GPIO 47 Mode: Input
GPIO 48 Mode: Input
GPIO 49 Mode: Input
GPIO 50 Mode: Input
GPIO 51 Mode: Input
GPIO 52 Mode: Input
```

#### T-1000 (Rasbian)

```shell
root@t-1000:~/edgecontroller# python3 ./get-line-mode.py
GPIO 00 Mode: Input
GPIO 01 Mode: Input
GPIO 02 Mode: Alt0
GPIO 03 Mode: Alt0
GPIO 04 Mode: Input
GPIO 05 Mode: Input
GPIO 06 Mode: Input
GPIO 07 Mode: Output
GPIO 08 Mode: Output
GPIO 09 Mode: Alt0
GPIO 10 Mode: Alt0
GPIO 11 Mode: Alt0
GPIO 12 Mode: Input
GPIO 13 Mode: Input
GPIO 14 Mode: Alt5
GPIO 15 Mode: Alt5
GPIO 16 Mode: Input
GPIO 17 Mode: Input
GPIO 18 Mode: Input
GPIO 19 Mode: Input
GPIO 20 Mode: Input
GPIO 21 Mode: Input
GPIO 22 Mode: Input
GPIO 23 Mode: Output
GPIO 24 Mode: Input
GPIO 25 Mode: Input
GPIO 26 Mode: Input
GPIO 27 Mode: Input
GPIO 28 Mode: Alt5
GPIO 29 Mode: Alt5
GPIO 30 Mode: Alt3
GPIO 31 Mode: Alt3
GPIO 32 Mode: Alt3
GPIO 33 Mode: Alt3
GPIO 34 Mode: Alt3
GPIO 35 Mode: Alt3
GPIO 36 Mode: Alt3
GPIO 37 Mode: Alt3
GPIO 38 Mode: Alt3
GPIO 39 Mode: Alt3
GPIO 40 Mode: Alt0
GPIO 41 Mode: Alt0
GPIO 42 Mode: Output
GPIO 43 Mode: Input
GPIO 44 Mode: Input
GPIO 45 Mode: Input
GPIO 46 Mode: Input
GPIO 47 Mode: Input
GPIO 48 Mode: Input
GPIO 49 Mode: Input
GPIO 50 Mode: Input
GPIO 51 Mode: Input
GPIO 52 Mode: Input
```

</details>








## Important Hardware access

- [ ] Camera access
- [ ] Distance sensor access
- [ ] Control the motors (via SPI)

## Scrabble

### Started with an Fedora Workstation installation



### Enable `iomem=relaxed` (add to boot parameter)

TBD

Import for `get-line-mode.py` and `set-line-mode.py`

### How to get /dev/spidev0.1


SPI device is disabled:

```shell

root@robocop:~# ls -lda /sys/firmware/devicetree/base/soc/spi@7e2*
drwxr-xr-x. 2 root root 0 Mar 18 15:47 /sys/firmware/devicetree/base/soc/spi@7e204000
drwxr-xr-x. 2 root root 0 Mar 18 15:47 /sys/firmware/devicetree/base/soc/spi@7e204600
drwxr-xr-x. 2 root root 0 Mar 18 15:47 /sys/firmware/devicetree/base/soc/spi@7e204800
drwxr-xr-x. 2 root root 0 Mar 18 15:47 /sys/firmware/devicetree/base/soc/spi@7e204a00
drwxr-xr-x. 2 root root 0 Mar 18 15:47 /sys/firmware/devicetree/base/soc/spi@7e204c00
drwxr-xr-x. 2 root root 0 Mar 18 15:47 /sys/firmware/devicetree/base/soc/spi@7e215080
drwxr-xr-x. 2 root root 0 Mar 18 15:47 /sys/firmware/devicetree/base/soc/spi@7e2150c0
root@robocop:~# cat /sys/firmware/devicetree/base/soc/spi@7e204000/status
disabledroot@robocop:~#
root@robocop:~# cat /sys/firmware/devicetree/base/soc/spi@7e204000/status ; echo
disabled
root@robocop:~# cat /sys/firmware/devicetree/base/soc/spi@7e204000/status ; echo
disabled
root@robocop:~#



root@t-1000:/boot# ls -lda /sys/firmware/devicetree/base/soc/spi@7e2*
drwxr-xr-x 4 root root 0 Mar 18 19:45 /sys/firmware/devicetree/base/soc/spi@7e204000
drwxr-xr-x 2 root root 0 Mar 18 19:45 /sys/firmware/devicetree/base/soc/spi@7e204600
drwxr-xr-x 2 root root 0 Mar 18 19:45 /sys/firmware/devicetree/base/soc/spi@7e204800
drwxr-xr-x 2 root root 0 Mar 18 19:45 /sys/firmware/devicetree/base/soc/spi@7e204a00
drwxr-xr-x 2 root root 0 Mar 18 19:45 /sys/firmware/devicetree/base/soc/spi@7e204c00
drwxr-xr-x 2 root root 0 Mar 18 19:45 /sys/firmware/devicetree/base/soc/spi@7e215080
drwxr-xr-x 2 root root 0 Mar 18 19:45 /sys/firmware/devicetree/base/soc/spi@7e2150c0
root@t-1000:/boot# cat /sys/firmware/devicetree/base/soc/spi@7e204000/status ; echo
okay
root@t-1000:/boot#

```

=> force enable it:

```shell
fdtput --type s /boot/dtb/broadcom/bcm2711-rpi-4-b.dtb /soc/spi@7e204000 status "okay"
```

=> dmesg
```
[    2.916265] spi-bcm2835 fe204000.spi: error -ENODEV: no tx-dma configuration found - not using dma mode
```



Looks like the raspberry pi kernel/device tree is prepared for the device.

Dump device tree the the robotos:
```
dtc -I fs /proc/device-tree > /tmp/t-1000.dtdump
```

Let's compare `spi@7e204000`

Robot with Fedora:
```shell
cat robocop.dtdump | grep -i 'spi@7e204000 {' -A35
                spi@7e204000 {
                        #address-cells = <0x01>;
                        interrupts = <0x00 0x76 0x04>;
                        clocks = <0x07 0x14>;
                        #size-cells = <0x00>;
                        compatible = "brcm,bcm2835-spi";
                        status = "okay";
                        reg = <0x7e204000 0x200>;
                        phandle = <0x81>;
                };

                dpi@7e208000 {
                        clock-names = "core", "pixel";
```

Robot with Rasbian
```shell
cat t-1000.dtdump | grep -i 'spi@7e204000 {' -A35
                spi@7e204000 {
                        pinctrl-names = "default";
                        #address-cells = <0x01>;
                        pinctrl-0 = <0x0e 0x0f>;
                        interrupts = <0x00 0x76 0x04>;
                        clocks = <0x08 0x14>;
                        #size-cells = <0x00>;
                        dma-names = "tx\0rx";
                        compatible = "brcm,bcm2835-spi";
                        status = "okay";
                        reg = <0x7e204000 0x200>;
                        phandle = <0x34>;
                        dmas = <0x0c 0x06 0x0c 0x07>;
                        cs-gpios = <0x07 0x08 0x01 0x07 0x07 0x01>;

                        spidev@0 {
                                #address-cells = <0x01>;
                                #size-cells = <0x00>;
                                spi-max-frequency = <0x7735940>;
                                compatible = "spidev";
                                reg = <0x00>;
                                phandle = <0xb0>;
                        };

                        spidev@1 {
                                #address-cells = <0x01>;
                                #size-cells = <0x00>;
                                spi-max-frequency = <0x7735940>;
                                compatible = "spidev";
                                reg = <0x01>;
                                phandle = <0xb1>;
                        };
                };

                dpi@7e208000 {
                        #address-cells = <0x01>;

```

![Image](https://github.com/user-attachments/assets/718e305a-1606-4651-b761-f33e7396585f)

raspberrypi kernel: https://github.com/raspberrypi/linux/blob/rpi-5.15.y/arch/arm/boot/dts/bcm2711-rpi-4-b.dts#L326-L346

vs upstream: https://github.com/torvalds/linux/blob/master/arch/arm/boot/dts/broadcom/bcm2711-rpi-4-b.dts spidev0: spidev@0 is missing



Looks like this was a problem with Pi 3 as well: https://freeshell.de/less/post/fedorarpispi/



<details>
<summary>Let's try the kernel stuff</summary>

https://freeshell.de/less/post/fedorarpispi/

```shell
% dnf install -y rpmdevtools
% dnf builddep -y kernel
% dnf download --source kernel
% rpm -i kernel-*.src.rpm
% cd rpmbuild

root@robocop:~/rpmbuild# rpmbuild -bp SPECS/kernel.spec

setting SOURCE_DATE_EPOCH=1741824000
error: Failed build dependencies:
        opencsd-devel >= 1.0.0 is needed by kernel-6.13.7-200.fc41.aarch64


dnf install -t opencsd-devel

rpmbuild -bp SPECS/kernel.spec




cd /root/rpmbuild/BUILD/kernel-6.13.7-build/kernel-6.13.7/linux-6.13.7/arch/arm/boot/dts/broadcom

curl https://raw.githubusercontent.com/raspberrypi/linux/refs/heads/rpi-6.13.y/arch/arm/boot/dts/broadcom/bcm2711-rpi-4-b.dts
..


cpp -I../../../include -nostdinc -undef -x assembler-with-cpp   bcm2711-rpi-4-b.dts > preprocessed.dts
dtc -I dts -O dtb -o bcm2711-rpi-4-b.dtb preprocessed.dts

dtc -I dts -O dtb -o bcm2711-rpi-4-b.dtb preprocessed.dts
Error: bcm2711-rpi-ds.dtsi:152.1-10 Label or path hevc_dec not found
FATAL ERROR: Syntax error parsing input tree

curl -L -O https://raw.githubusercontent.com/raspberrypi/linux/refs/heads/rpi-6.13.y/arch/arm/boot/dts/broadcom/bcm2711-rpi-ds.dtsi
curl -L -O https://raw.githubusercontent.com/raspberrypi/linux/refs/heads/rpi-6.13.y/arch/arm/boot/dts/broadcom/bcm2711.dtsi

  474  cpp -I../../../include -nostdinc -undef -x assembler-with-cpp   bcm2711-rpi-4-b.dts > preprocessed.dts
  475  dtc -I dts -O dtb -o bcm2711-rpi-4-b.dtb preprocessed.dts

  root@robocop:~/rpmbuild/BUILD/kernel-6.13.7-build/kernel-6.13.7/linux-6.13.7/arch/arm/boot/dts/broadcom# cp /boot/dtb/broadcom/bcm2711-rpi-4-b.dtb /boot/dtb/broadcom/bcm2711-rpi-4-b.dtb.ORIG
cp: overwrite '/boot/dtb/broadcom/bcm2711-rpi-4-b.dtb.ORIG'? y
root@robocop:~/rpmbuild/BUILD/kernel-6.13.7-build/kernel-6.13.7/linux-6.13.7/arch/arm/boot/dts/broadcom# cp bcm2711-rpi-4-b.dtb /boot/dtb/broadcom/bcm2711-rpi-4-b.dtb
cp: overwrite '/boot/dtb/broadcom/bcm2711-rpi-4-b.dtb'? y
root@robocop:~/rpmbuild/BUILD/kernel-6.13.7-build/kernel-6.13.7/linux-6.13.7/arch/arm/boot/dts/broadcom# md5sum /boot/dtb/broadcom/bcm2711-rpi-4-b.dtb*
560ebcc3bf3aae7cac7402d76fe784d0  /boot/dtb/broadcom/bcm2711-rpi-4-b.dtb
c7e824402ffc224c7a566832f9c67e39  /boot/dtb/broadcom/bcm2711-rpi-4-b.dtb.ORIG
root@robocop:~/rpmbuild/BUILD/kernel-6.13.7-build/kernel-6.13.7/linux-6.13.7/arch/arm/boot/dts/broadcom#

reboot

fdtput --type s /boot/dtb/broadcom/bcm2711-rpi-4-b.dtb /soc/spi@7e204000 status "okay"

echo spidev > /sys/bus/spi/devices/spi0.1/driver_override
echo spidev > /sys/bus/spi/devices/spi0.0/driver_override
echo spi0.0 > /sys/bus/spi/drivers/spidev/bind
echo spi0.1 > /sys/bus/spi/drivers/spidev/bind

root@robocop:~/fedora-iot-raspberry-pi# ls -la /dev/spidev*
crw-------. 1 root root 153, 0 Mar 19 07:24 /dev/spidev0.0
crw-------. 1 root root 153, 1 Mar 19 07:24 /dev/spidev0.1
root@robocop:~/fedora-iot-raspberry-pi#

```

Kernel: 6.13.6-200.fc41.aarch64

Upstream: https://raw.githubusercontent.com/torvalds/linux/refs/tags/v6.13/arch/arm/boot/dts/broadcom/bcm2711-rpi-4-b.dts
Raspian: https://raw.githubusercontent.com/raspberrypi/linux/refs/heads/rpi-6.13.y/arch/arm/boot/dts/broadcom/bcm2711-rpi-4-b.dts

</details>