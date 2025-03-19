# Diff between bcm2711-rpi-4-b.dts upstream and rasbian (kernel v6.13x)

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