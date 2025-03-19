# Diff between bcm2711-rpi-4-b.dts upstream and rasbian (kernel v6.13x)

<details>
<summary>File: bcm2711-rpi-4-b.dts</summary>

```diff
diff -Nuar <( curl -s https://raw.githubusercontent.com/torvalds/linux/refs/tags/v6.13/arch/arm/boot/dts/broadcom/bcm2711-rpi-4-b.dts) <( curl -s https://raw.githubusercontent.com/raspberrypi/linux/refs/heads/rpi-6.13.y/arch/arm/boot/dts/broadcom/bcm2711-rpi-4-b.dts)
--- /dev/fd/11  2025-03-19 10:18:01.834007626 +0100
+++ /dev/fd/12  2025-03-19 10:18:01.834498171 +0100
@@ -1,11 +1,19 @@
 // SPDX-License-Identifier: GPL-2.0
 /dts-v1/;
+#define BCM2711
+#define i2c0 i2c0if
 #include "bcm2711.dtsi"
 #include "bcm2711-rpi.dtsi"
+/delete-node/&i2c0mux;
 #include "bcm283x-rpi-led-deprecated.dtsi"
-#include "bcm283x-rpi-usb-peripheral.dtsi"
 #include "bcm283x-rpi-wifi-bt.dtsi"
 #include <dt-bindings/leds/common.h>
+#undef i2c0
+#include "bcm270x.dtsi"
+#define i2c0 i2c0mux
+#undef i2c0
+
+/delete-node/ &cam1_reg;

 / {
        compatible = "raspberrypi,4-model-b", "brcm,bcm2711";
@@ -68,7 +76,7 @@
                          "VDD_SD_IO_SEL",
                          "CAM_GPIO",           /*  5 */
                          "SD_PWR_ON",
-                         "";
+                         "SD_OC_N";
 };

 &gpio {
@@ -82,21 +90,21 @@
         */
        gpio-line-names = "ID_SDA",             /*  0 */
                          "ID_SCL",
-                         "SDA1",
-                         "SCL1",
-                         "GPIO_GCLK",
+                         "GPIO2",
+                         "GPIO3",
+                         "GPIO4",
                          "GPIO5",              /*  5 */
                          "GPIO6",
-                         "SPI_CE1_N",
-                         "SPI_CE0_N",
-                         "SPI_MISO",
-                         "SPI_MOSI",           /* 10 */
-                         "SPI_SCLK",
+                         "GPIO7",
+                         "GPIO8",
+                         "GPIO9",
+                         "GPIO10",             /* 10 */
+                         "GPIO11",
                          "GPIO12",
                          "GPIO13",
                          /* Serial port */
-                         "TXD1",
-                         "RXD1",               /* 15 */
+                         "GPIO14",
+                         "GPIO15",             /* 15 */
                          "GPIO16",
                          "GPIO17",
                          "GPIO18",
@@ -214,7 +222,7 @@
                        led@0 {
                                reg = <0>;
                                color = <LED_COLOR_ID_GREEN>;
-                               function = LED_FUNCTION_LAN;
+                               function = "lan";//LED_FUNCTION_LAN;
                                default-state = "keep";
                        };

@@ -222,7 +230,7 @@
                        led@1 {
                                reg = <1>;
                                color = <LED_COLOR_ID_AMBER>;
-                               function = LED_FUNCTION_LAN;
+                               function = "lan";//LED_FUNCTION_LAN;
                                default-state = "keep";
                        };
                };
@@ -270,3 +278,233 @@
 &wifi_pwrseq {
        reset-gpios = <&expgpio 1 GPIO_ACTIVE_LOW>;
 };
+
+// =============================================
+// Downstream rpi- changes
+
+#include "bcm271x-rpi-bt.dtsi"
+
+/ {
+       soc {
+               /delete-node/ pixelvalve@7e807000;
+               /delete-node/ hdmi@7e902000;
+       };
+};
+
+&phy1 {
+       /delete-node/ leds;
+};
+
+#include "bcm2711-rpi-ds.dtsi"
+#include "bcm283x-rpi-csi1-2lane.dtsi"
+#include "bcm283x-rpi-i2c0mux_0_44.dtsi"
+
+/ {
+       /delete-node/ wifi-pwrseq;
+};
+
+&mmcnr {
+       pinctrl-names = "default";
+       pinctrl-0 = <&sdio_pins>;
+       bus-width = <4>;
+       status = "okay";
+};
+
+&uart0 {
+       pinctrl-0 = <&uart0_pins &bt_pins>;
+       status = "okay";
+};
+
+&uart1 {
+       pinctrl-0 = <&uart1_pins>;
+};
+
+&spi0 {
+       pinctrl-names = "default";
+       pinctrl-0 = <&spi0_pins &spi0_cs_pins>;
+       cs-gpios = <&gpio 8 1>, <&gpio 7 1>;
+
+       spidev0: spidev@0{
+               compatible = "spidev";
+               reg = <0>;      /* CE0 */
+               #address-cells = <1>;
+               #size-cells = <0>;
+               spi-max-frequency = <125000000>;
+       };
+
+       spidev1: spidev@1{
+               compatible = "spidev";
+               reg = <1>;      /* CE1 */
+               #address-cells = <1>;
+               #size-cells = <0>;
+               spi-max-frequency = <125000000>;
+       };
+};
+
+&gpio {
+       gpio-line-names = "ID_SDA",
+                         "ID_SCL",
+                         "GPIO2",
+                         "GPIO3",
+                         "GPIO4",
+                         "GPIO5",
+                         "GPIO6",
+                         "GPIO7",
+                         "GPIO8",
+                         "GPIO9",
+                         "GPIO10",
+                         "GPIO11",
+                         "GPIO12",
+                         "GPIO13",
+                         "GPIO14",
+                         "GPIO15",
+                         "GPIO16",
+                         "GPIO17",
+                         "GPIO18",
+                         "GPIO19",
+                         "GPIO20",
+                         "GPIO21",
+                         "GPIO22",
+                         "GPIO23",
+                         "GPIO24",
+                         "GPIO25",
+                         "GPIO26",
+                         "GPIO27",
+                         "RGMII_MDIO",
+                         "RGMIO_MDC",
+                         /* Used by BT module */
+                         "CTS0",               /* 30 */
+                         "RTS0",
+                         "TXD0",
+                         "RXD0",
+                         /* Used by Wifi */
+                         "SD1_CLK",
+                         "SD1_CMD",            /* 35 */
+                         "SD1_DATA0",
+                         "SD1_DATA1",
+                         "SD1_DATA2",
+                         "SD1_DATA3",
+                         /* Shared with SPI flash */
+                         "PWM0_MISO",          /* 40 */
+                         "PWM1_MOSI",
+                         "STATUS_LED_G_CLK",
+                         "SPIFLASH_CE_N",
+                         "SDA0",
+                         "SCL0",               /* 45 */
+                         "RGMII_RXCLK",
+                         "RGMII_RXCTL",
+                         "RGMII_RXD0",
+                         "RGMII_RXD1",
+                         "RGMII_RXD2",         /* 50 */
+                         "RGMII_RXD3",
+                         "RGMII_TXCLK",
+                         "RGMII_TXCTL",
+                         "RGMII_TXD0",
+                         "RGMII_TXD1",         /* 55 */
+                         "RGMII_TXD2",
+                         "RGMII_TXD3";
+
+       bt_pins: bt_pins {
+               brcm,pins = "-"; // non-empty to keep btuart happy, //4 = 0
+                                // to fool pinctrl
+               brcm,function = <0>;
+               brcm,pull = <2>;
+       };
+
+       uart0_pins: uart0_pins {
+               brcm,pins = <32 33>;
+               brcm,function = <BCM2835_FSEL_ALT3>;
+               brcm,pull = <0 2>;
+       };
+
+       uart1_pins: uart1_pins {
+               brcm,pins;
+               brcm,function;
+               brcm,pull;
+       };
+
+       uart1_bt_pins: uart1_bt_pins {
+               brcm,pins = <32 33 30 31>;
+               brcm,function = <BCM2835_FSEL_ALT5>; /* alt5=UART1 */
+               brcm,pull = <0 2 2 0>;
+       };
+};
+
+&i2c0if {
+       clock-frequency = <100000>;
+};
+
+&i2c1 {
+       pinctrl-names = "default";
+       pinctrl-0 = <&i2c1_pins>;
+       clock-frequency = <100000>;
+};
+
+&i2s {
+       pinctrl-names = "default";
+       pinctrl-0 = <&i2s_pins>;
+};
+
+// =============================================
+// Board specific stuff here
+
+&sdhost {
+       status = "disabled";
+};
+
+&phy1 {
+       led-modes = <0x00 0x08>; /* link/activity link */
+};
+
+&gpio {
+       audio_pins: audio_pins {
+               brcm,pins = <40 41>;
+               brcm,function = <4>;
+               brcm,pull = <0>;
+       };
+};
+
+&led_act {
+       default-state = "off";
+       linux,default-trigger = "mmc0";
+};
+
+&led_pwr {
+       default-state = "off";
+};
+
+&pwm1 {
+       status = "disabled";
+};
+
+&vchiq {
+       pinctrl-names = "default";
+       pinctrl-0 = <&audio_pins>;
+};
+
+&cam1_reg {
+       gpio = <&expgpio 5 GPIO_ACTIVE_HIGH>;
+};
+
+cam0_reg: &cam_dummy_reg {
+};
+
+i2c_csi_dsi0: &i2c0 {
+};
+
+/ {
+       __overrides__ {
+               audio = <&chosen>,"bootargs{on='snd_bcm2835.enable_headphones=1 snd_bcm2835.enable_hdmi=1',off='snd_bcm2835.enable_headphones=0 snd_bcm2835.enable_hdmi=0'}";
+
+               act_led_gpio = <&led_act>,"gpios:4";
+               act_led_activelow = <&led_act>,"gpios:8";
+               act_led_trigger = <&led_act>,"linux,default-trigger";
+
+               pwr_led_gpio = <&led_pwr>,"gpios:4";
+               pwr_led_activelow = <&led_pwr>,"gpios:8";
+               pwr_led_trigger = <&led_pwr>,"linux,default-trigger";
+
+               eth_led0 = <&phy1>,"led-modes:0";
+               eth_led1 = <&phy1>,"led-modes:4";
+       };
+};
```

</details>


<details>
<summary>File: bcm270x-rpi.dtsi</summary>

```diff
export FILE=bcm270x-rpi.dtsi; diff -Nuar <( curl -s https://raw.githubusercontent.com/torvalds/linux/refs/tags/v6.13/arch/arm/boot/dts/broadcom/$FILE) <( curl -s https://raw.githubusercontent.com/raspberrypi/linux/refs/heads/rpi-6.13.y/arch/arm/boot/dts/broadcom/$FILE)
--- /dev/fd/11  2025-03-19 10:27:30.483026079 +0100
+++ /dev/fd/12  2025-03-19 10:27:30.484156961 +0100
@@ -1 +1,201 @@
-404: Not Found
\ No newline at end of file
+/* Downstream modifications to bcm2835-rpi.dtsi */
+
+/ {
+       aliases: aliases {
+               aux = &aux;
+               sound = &sound;
+               soc = &soc;
+               dma = &dma;
+               intc = &intc;
+               watchdog = &watchdog;
+               random = &random;
+               mailbox = &mailbox;
+               gpio = &gpio;
+               uart0 = &uart0;
+               uart1 = &uart1;
+               sdhost = &sdhost;
+               mmc = &mmc;
+               mmc1 = &mmc;
+               mmc0 = &sdhost;
+               i2s = &i2s;
+               i2c0 = &i2c0;
+               i2c1 = &i2c1;
+               i2c10 = &i2c_csi_dsi;
+               i2c = &i2c_arm;
+               spi0 = &spi0;
+               spi1 = &spi1;
+               spi2 = &spi2;
+               usb = &usb;
+               leds = &leds;
+               fb = &fb;
+               thermal = &thermal;
+               axiperf = &axiperf;
+       };
+
+       /* Define these notional regulators for use by overlays */
+       vdd_3v3_reg: fixedregulator_3v3 {
+               compatible = "regulator-fixed";
+               regulator-always-on;
+               regulator-max-microvolt = <3300000>;
+               regulator-min-microvolt = <3300000>;
+               regulator-name = "3v3";
+       };
+
+       vdd_5v0_reg: fixedregulator_5v0 {
+               compatible = "regulator-fixed";
+               regulator-always-on;
+               regulator-max-microvolt = <5000000>;
+               regulator-min-microvolt = <5000000>;
+               regulator-name = "5v0";
+       };
+
+       soc {
+               gpiomem {
+                       compatible = "brcm,bcm2835-gpiomem";
+                       reg = <0x7e200000 0x1000>;
+               };
+
+               fb: fb {
+                       compatible = "brcm,bcm2708-fb";
+                       firmware = <&firmware>;
+                       status = "okay";
+               };
+
+               /* External sound card */
+               sound: sound {
+                       status = "disabled";
+               };
+       };
+
+       __overrides__ {
+               cache_line_size;
+
+               uart0 = <&uart0>,"status";
+               uart1 = <&uart1>,"status";
+               i2s = <&i2s>,"status";
+               spi = <&spi0>,"status";
+               i2c0 = <&i2c0if>,"status",<&i2c0mux>,"status";
+               i2c1 = <&i2c1>,"status";
+               i2c = <&i2c1>,"status";
+               i2c_arm = <&i2c1>,"status";
+               i2c_vc = <&i2c0if>,"status",<&i2c0mux>,"status";
+               i2c0_baudrate = <&i2c0if>,"clock-frequency:0";
+               i2c1_baudrate = <&i2c1>,"clock-frequency:0";
+               i2c_baudrate = <&i2c1>,"clock-frequency:0";
+               i2c_arm_baudrate = <&i2c1>,"clock-frequency:0";
+               i2c_vc_baudrate = <&i2c0if>,"clock-frequency:0";
+
+               watchdog = <&watchdog>,"status";
+               random = <&random>,"status";
+               sd_overclock = <&sdhost>,"brcm,overclock-50:0";
+               sd_force_pio = <&sdhost>,"brcm,force-pio?";
+               sd_pio_limit = <&sdhost>,"brcm,pio-limit:0";
+               sd_debug     = <&sdhost>,"brcm,debug";
+               sdio_overclock = <&mmc>,"brcm,overclock-50:0",
+                                <&mmcnr>,"brcm,overclock-50:0";
+               axiperf      = <&axiperf>,"status";
+               drm_fb0_vc4 = <&aliases>, "drm-fb0=",&vc4;
+               drm_fb1_vc4 = <&aliases>, "drm-fb1=",&vc4;
+               drm_fb2_vc4 = <&aliases>, "drm-fb2=",&vc4;
+
+               cam1_sync = <&csi1>, "sync-gpios:0=", <&gpio>,
+                           <&csi1>, "sync-gpios:4",
+                           <&csi1>, "sync-gpios:8=", <GPIO_ACTIVE_HIGH>;
+               cam1_sync_inverted = <&csi1>, "sync-gpios:0=", <&gpio>,
+                           <&csi1>, "sync-gpios:4",
+                           <&csi1>, "sync-gpios:8=", <GPIO_ACTIVE_LOW>;
+               cam0_sync = <&csi0>, "sync-gpios:0=", <&gpio>,
+                           <&csi0>, "sync-gpios:4",
+                           <&csi0>, "sync-gpios:8=", <GPIO_ACTIVE_HIGH>;
+               cam0_sync_inverted = <&csi0>, "sync-gpios:0=", <&gpio>,
+                           <&csi0>, "sync-gpios:4",
+                           <&csi0>, "sync-gpios:8=", <GPIO_ACTIVE_LOW>;
+
+               cam0_reg = <&cam0_reg>,"status";
+               cam0_reg_gpio = <&cam0_reg>,"gpio:4",
+                               <&cam0_reg>,"gpio:0=", <&gpio>;
+               cam1_reg = <&cam1_reg>,"status";
+               cam1_reg_gpio = <&cam1_reg>,"gpio:4",
+                               <&cam1_reg>,"gpio:0=", <&gpio>;
+
+               strict_gpiod = <&chosen>, "bootargs=pinctrl_bcm2835.persist_gpio_outputs=n";
+       };
+};
+
+&uart0 {
+       skip-init;
+};
+
+&uart1 {
+       skip-init;
+};
+
+&txp {
+       status = "disabled";
+};
+
+&i2c0if {
+       status = "disabled";
+};
+
+&i2c0mux {
+       pinctrl-names = "i2c0", "i2c_csi_dsi";
+       /delete-property/ clock-frequency;
+       status = "disabled";
+};
+
+&i2c1 {
+       status = "disabled";
+};
+
+i2s_clk_producer: &i2s {};
+i2s_clk_consumer: &i2s {};
+
+&clocks {
+       firmware = <&firmware>;
+};
+
+&sdhci {
+       pinctrl-names = "default";
+       pinctrl-0 = <&emmc_gpio48>;
+       bus-width = <4>;
+};
+
+&cpu_thermal {
+       // Add some labels
+       thermal_trips: trips {
+               cpu-crit {
+                       // Raise upstream limit of 90C
+                       temperature = <110000>;
+               };
+       };
+       cooling_maps: cooling-maps {
+       };
+};
+
+&vec {
+       clocks = <&firmware_clocks 15>;
+       status = "disabled";
+};
+
+&firmware {
+       vcio: vcio {
+               compatible = "raspberrypi,vcio";
+       };
+};
+
+&vc4 {
+       raspberrypi,firmware = <&firmware>;
+};
+
+#ifndef BCM2711
+
+&hdmi {
+       reg-names = "hdmi",
+                   "hd";
+       clocks = <&firmware_clocks 9>,
+                <&firmware_clocks 13>;
+       dmas = <&dma (17|(1<<27)|(1<<24))>;
+};
+
+#endif
```
</details>

<details>
<summary>File: bcm2711.dtsi</summary>

```diff
 export FILE=bcm2711.dtsi; diff -Nuar <( curl -s https://raw.githubusercontent.com/torvalds/linux/refs/tags/v6.13/arch/arm/boot/dts/broadcom/$FILE) <( curl -s https://raw.githubusercontent.com/raspberrypi/linux/refs/heads/rpi-6.13.y/arch/arm/boot/dts/broadcom/$FILE)
--- /dev/fd/11  2025-03-19 10:35:36.995842843 +0100
+++ /dev/fd/12  2025-03-19 10:35:36.997120267 +0100
@@ -134,7 +134,7 @@
                        clocks = <&clocks BCM2835_CLOCK_UART>,
                                 <&clocks BCM2835_CLOCK_VPU>;
                        clock-names = "uartclk", "apb_pclk";
-                       arm,primecell-periphid = <0x00241011>;
+                       arm,primecell-periphid = <0x00341011>;
                        status = "disabled";
                };

@@ -145,7 +145,7 @@
                        clocks = <&clocks BCM2835_CLOCK_UART>,
                                 <&clocks BCM2835_CLOCK_VPU>;
                        clock-names = "uartclk", "apb_pclk";
-                       arm,primecell-periphid = <0x00241011>;
+                       arm,primecell-periphid = <0x00341011>;
                        status = "disabled";
                };

@@ -156,7 +156,7 @@
                        clocks = <&clocks BCM2835_CLOCK_UART>,
                                 <&clocks BCM2835_CLOCK_VPU>;
                        clock-names = "uartclk", "apb_pclk";
-                       arm,primecell-periphid = <0x00241011>;
+                       arm,primecell-periphid = <0x00341011>;
                        status = "disabled";
                };

@@ -167,7 +167,7 @@
                        clocks = <&clocks BCM2835_CLOCK_UART>,
                                 <&clocks BCM2835_CLOCK_VPU>;
                        clock-names = "uartclk", "apb_pclk";
-                       arm,primecell-periphid = <0x00241011>;
+                       arm,primecell-periphid = <0x00341011>;
                        status = "disabled";
                };

@@ -277,7 +277,7 @@
                        reg = <0x7e20c800 0x28>;
                        clocks = <&clocks BCM2835_CLOCK_PWM>;
                        assigned-clocks = <&clocks BCM2835_CLOCK_PWM>;
-                       assigned-clock-rates = <10000000>;
+                       assigned-clock-rates = <50000000>;
                        #pwm-cells = <3>;
                        status = "disabled";
                };
@@ -451,8 +451,6 @@
                                          IRQ_TYPE_LEVEL_LOW)>,
                             <GIC_PPI 10 (GIC_CPU_MASK_SIMPLE(4) |
                                          IRQ_TYPE_LEVEL_LOW)>;
-               /* This only applies to the ARMv7 stub */
-               arm,cpu-registers-not-fw-configured;
        };

        cpus: cpus {
@@ -604,20 +602,6 @@
                        };
                };

-               xhci: usb@7e9c0000 {
-                       compatible = "brcm,bcm2711-xhci", "brcm,xhci-brcm-v2";
-                       reg = <0x0 0x7e9c0000 0x100000>;
-                       #address-cells = <1>;
-                       #size-cells = <0>;
-                       interrupts = <GIC_SPI 176 IRQ_TYPE_LEVEL_HIGH>;
-                       /* DWC2 and this IP block share the same USB PHY,
-                        * enabling both at the same time results in lockups.
-                        * So keep this node disabled and let the bootloader
-                        * decide which interface should be enabled.
-                        */
-                       status = "disabled";
-               };
-
                v3d: gpu@7ec00000 {
                        compatible = "brcm,2711-v3d";
                        reg = <0x0 0x7ec00000 0x4000>,
@@ -628,6 +612,15 @@
                        resets = <&pm BCM2835_RESET_V3D>;
                        interrupts = <GIC_SPI 74 IRQ_TYPE_LEVEL_HIGH>;
                };
+
+               hevc_dec: codec@7eb10000 {
+                       compatible = "brcm,bcm2711-hevc-dec", "raspberrypi,hevc-dec";
+                       reg = <0x0 0x7eb00000  0x10000>, /* HEVC */
+                             <0x0 0x7eb10000  0x1000>;  /* INTC */
+                       reg-names = "hevc",
+                                   "intc";
+                       interrupts = <GIC_SPI 98 IRQ_TYPE_LEVEL_HIGH>;
+               };
        };
 };

@@ -1177,6 +1170,7 @@
 };

 &uart0 {
+       arm,primecell-periphid = <0x00341011>;
        interrupts = <GIC_SPI 121 IRQ_TYPE_LEVEL_HIGH>;
 };
```
</details>

<details>
<summary>File: bcm2711-rpi.dtsi</summary>

```diff
export FILE=bcm2711-rpi.dtsi; diff -Nuar <( curl -s https://raw.githubusercontent.com/torvalds/linux/refs/tags/v6.13/arch/arm/boot/dts/broadcom/$FILE) <( curl -s https://raw.githubusercontent.com/raspberrypi/linux/refs/heads/rpi-6.13.y/arch/arm/boot/dts/broadcom/$FILE)
--- /dev/fd/11  2025-03-19 10:37:31.568223098 +0100
+++ /dev/fd/12  2025-03-19 10:37:31.569388146 +0100
@@ -1,7 +1,6 @@
 // SPDX-License-Identifier: GPL-2.0
 #include "bcm2835-rpi.dtsi"

-#include <dt-bindings/power/raspberrypi-power.h>
 #include <dt-bindings/reset/raspberrypi,firmware-reset.h>

 / {
@@ -16,6 +15,7 @@
                ethernet0 = &genet;
                pcie0 = &pcie0;
                blconfig = &blconfig;
+               blpubkey = &blpubkey;
        };

        i2c0mux: i2c-mux0 {
@@ -92,6 +92,18 @@
                no-map;
                status = "disabled";
        };
+       /*
+        * RPi4 will copy the binary public key blob (if present) from the bootloader
+        * into memory for use by the OS.
+        */
+       blpubkey: nvram@1 {
+               compatible = "raspberrypi,bootloader-public-key", "nvmem-rmem";
+               #address-cells = <1>;
+               #size-cells = <1>;
+               reg = <0x0 0x0 0x0>;
+               no-map;
+               status = "disabled";
+       };
 };

 &v3d {
@@ -102,6 +114,6 @@
        interrupts = <GIC_SPI 34 IRQ_TYPE_LEVEL_HIGH>;
 };

-&xhci {
-       power-domains = <&power RPI_POWER_DOMAIN_USB>;
+&hevc_dec {
+       clocks = <&firmware_clocks 11>;
 };
```
</details>

<details>
<summary>File: xxx</summary>

```diff
```
</details>
