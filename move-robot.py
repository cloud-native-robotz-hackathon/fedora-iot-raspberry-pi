#!/usr/bin/env python

# https://github.com/raspberrypi/documentation/blob/develop/documentation/asciidoc/computers/raspberry-pi/spi-bus-on-raspberry-pi.adoc

import spidev

GPG_SPI = spidev.SpiDev()
GPG_SPI.open(0, 1)
GPG_SPI.max_speed_hz = 500000
GPG_SPI.mode = 0b00
GPG_SPI.bits_per_word = 8

MOTOR_GEAR_RATIO           = 120 # Motor gear ratio # 220 for Nicole's prototype
ENCODER_TICKS_PER_ROTATION = 6   # Encoder ticks per motor rotation (number of magnet positions) # 16 for early prototypes
MOTOR_TICKS_PER_DEGREE = ((MOTOR_GEAR_RATIO * ENCODER_TICKS_PER_ROTATION) / 360.0) # encoder ticks per output shaft rotation degree
MOTOR_LEFT  = 0x01
MOTOR_RIGHT = 0x02
DEFAULT_SPEED = 300
NO_LIMIT_SPEED = 1000

SPI_Address = 8


class Enumeration(object):
    def __init__(self, names):  # or *names, with no .split()
        number = 0
        for _, name in enumerate(names.split('\n')):
            if name.find(",") >= 0:
                # strip out the spaces
                while(name.find(" ") != -1):
                    name = name[:name.find(" ")] + name[(name.find(" ") + 1):]

                # strip out the commas
                while(name.find(",") != -1):
                    name = name[:name.find(",")] + name[(name.find(",") + 1):]

                # if the value was specified
                if(name.find("=") != -1):
                    number = int(float(name[(name.find("=") + 1):]))
                    name = name[:name.find("=")]

                # optionally print to confirm that it's working correctly
                print("%40s has a value of %d" % (name, number))

                setattr(self, name, number)
                number = number + 1


SPI_MESSAGE_TYPE = Enumeration("""
    NONE,

    GET_MANUFACTURER,
    GET_NAME,
    GET_HARDWARE_VERSION,
    GET_FIRMWARE_VERSION,
    GET_ID,

    SET_LED,

    GET_VOLTAGE_5V,
    GET_VOLTAGE_VCC,

    SET_SERVO,

    SET_MOTOR_PWM,

    SET_MOTOR_POSITION,
    SET_MOTOR_POSITION_KP,
    SET_MOTOR_POSITION_KD,

    SET_MOTOR_DPS,

    SET_MOTOR_LIMITS,

    OFFSET_MOTOR_ENCODER,

    GET_MOTOR_ENCODER_LEFT,
    GET_MOTOR_ENCODER_RIGHT,

    GET_MOTOR_STATUS_LEFT,
    GET_MOTOR_STATUS_RIGHT,

    SET_GROVE_TYPE,
    SET_GROVE_MODE,
    SET_GROVE_STATE,
    SET_GROVE_PWM_DUTY,
    SET_GROVE_PWM_FREQUENCY,

    GET_GROVE_VALUE_1,
    GET_GROVE_VALUE_2,
    GET_GROVE_STATE_1_1,
    GET_GROVE_STATE_1_2,
    GET_GROVE_STATE_2_1,
    GET_GROVE_STATE_2_2,
    GET_GROVE_VOLTAGE_1_1,
    GET_GROVE_VOLTAGE_1_2,
    GET_GROVE_VOLTAGE_2_1,
    GET_GROVE_VOLTAGE_2_2,
    GET_GROVE_ANALOG_1_1,
    GET_GROVE_ANALOG_1_2,
    GET_GROVE_ANALOG_2_1,
    GET_GROVE_ANALOG_2_2,

    START_GROVE_I2C_1,
    START_GROVE_I2C_2,
""")

def set_motor_dps(port, dps):
    """
    Set the motor target speed in degrees per second

    Keyword arguments:
    port -- The motor port(s). MOTOR_LEFT and/or MOTOR_RIGHT.
    dps -- The target speed in degrees per second
    """
    dps = int(dps * MOTOR_TICKS_PER_DEGREE)
    outArray = [SPI_Address, SPI_MESSAGE_TYPE.SET_MOTOR_DPS, int(port),\
                ((dps >> 8) & 0xFF), (dps & 0xFF)]
    return GPG_SPI.xfer2(outArray)

print(set_motor_dps(MOTOR_LEFT + MOTOR_RIGHT, NO_LIMIT_SPEED))

print(GPG_SPI.xfer2([SPI_Address, 6, 0, 0, 0, 0]))


reply = GPG_SPI.xfer2([SPI_Address, SPI_MESSAGE_TYPE.GET_MOTOR_STATUS_LEFT, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

if(reply[3] == 0xA5):
    power = int(reply[5])
    if power & 0x80:
        power = power - 0x100

    encoder = int((reply[6] << 24) | (reply[7] << 16) | (reply[8] << 8) | reply[9])
    if encoder & 0x80000000:
        encoder = int(encoder - 0x100000000)

    dps = int((reply[10] << 8) | reply[11])
    if dps & 0x8000:
        dps = dps - 0x10000

    print([reply[4], power, int(encoder / MOTOR_TICKS_PER_DEGREE), int(dps / MOTOR_TICKS_PER_DEGREE)])