#!/usr/bin/env bash


set -x 

echo spidev > /sys/bus/spi/devices/spi0.1/driver_override
echo spidev > /sys/bus/spi/devices/spi0.0/driver_override
echo spi0.0 > /sys/bus/spi/drivers/spidev/bind
echo spi0.1 > /sys/bus/spi/drivers/spidev/bind

ls -la /dev/spidev*

