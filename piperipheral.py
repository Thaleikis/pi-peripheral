#!/usr/bin/env python3

from signal import pause
from time import sleep
import RPi.GPIO as GPIO 

NULL_CHAR = chr(0)

# Byte 0 is for a modifier key, or combination thereof. It is used as a bitmap, each bit mapped to a modifier:
# bit 0: left control
# bit 1: left shift
# bit 2: left alt
# bit 3: left GUI (Win/Apple/Meta key)
# bit 4: right control
# bit 5: right shift
# bit 6: right alt
# bit 7: right GUI
MOD_NONE = NULL_CHAR
MOD_L_CNTR = chr(int('000000001', 2))
MOD_SHFT   = chr(int('000000010', 2))
MOD_ALT    = chr(int('000000100', 2))
MOD_R_CNTR = chr(int('000010000', 2))
KEY_NONE = 0

KEY_A = 4
KEY_B = 5
KEY_C = 6
KEY_D = 7
KEY_E = 8
KEY_F = 9
KEY_G = 10
KEY_H = 11
KEY_I = 12
KEY_J = 13
KEY_K = 14
KEY_L = 15
KEY_M = 16
KEY_N = 17
KEY_O = 18
KEY_P = 19
KEY_Q = 20
KEY_R = 21
KEY_S = 22
KEY_T = 23
KEY_U = 24
KEY_V = 25
KEY_W = 26
KEY_X = 27
KEY_Y = 29
KEY_Z = 28

KEY_F1  = 58
KEY_F2  = 59
KEY_F3  = 60
KEY_F4  = 61
KEY_F5  = 62
KEY_F6  = 63
KEY_F7  = 64
KEY_F8  = 65
KEY_F9  = 66
KEY_F10 = 67
KEY_F11 = 68
KEY_F12 = 69

# NUMPAD
KEY_KP0 = 82
KEY_KP1 = 79
KEY_KP2 = 80
KEY_KP3 = 81
KEY_KP4 = 75
KEY_KP5 = 76
KEY_KP6 = 77
KEY_KP7 = 71
KEY_KP8 = 72
KEY_KP9 = 73


KEY_NUMPAD_DEL = 99


# Key mapping in the form
# (GPIO_ID, (press-key,press-key-modifier, release-key,release-key-modifier)) 

#### Adjust the mappings to your needs, already configured mappings are examples
#### Grouping is based on GPIO Layout of Pi Zero W.
#### Connect one Contact to a Ground GPIO and the other to the matching GPIO Pin
#### An overview is added to the README
gpio_button_map = dict([
    # Group 2,3,4
    (2, (KEY_G, MOD_NONE, KEY_NONE, MOD_NONE))  # Button 2 Landing Gear
    , (3, (KEY_A, MOD_NONE, KEY_NONE, MOD_NONE))  # Button 3 Parking Break
    , (4, (KEY_F5, MOD_NONE, KEY_NONE, MOD_NONE))  # Button 4 Decrease Flaps
    
    # Group 5,6,13,19,26
#    , (5, ())
#    , (6, ())
#    , (13, ())
#    , (19, ())
#    , (26, ())
    
    # Group 7,8,25
#    , (7, ())
#    , (8, ())
#    , (25, ())
    
    # Group 9,10,11
#    , (9, ())
#    , (10, ())
#    , (11, ())
    
    # Group 12
#    , (12, ())
    
    # Group 14,15,18
#    , (14, ())
#    , (15, ())
#    , (18, ())
    
    # Group 16,20,21
#    , (16, ())
#    , (20, ())
#    , (21, ())
    
    # Group 17,22,27
    , (17, (KEY_F6, MOD_NONE, KEY_NONE, MOD_NONE))  # Switch 3 Increase Flaps
#    , (22, ())
    , (27, (KEY_Z, MOD_NONE, KEY_NONE, MOD_NONE))  # Button 2 Autopilot On/Off
    
    # Group 23,24
#    , (23, ())
#    , (24, ())

    # Group 12
#    , (12, ())
    # Group 16,20,21
#    , (16, ())
#    , (20, ())
#    , (21, ())

    ])


def write_report(report):
    with open('/dev/hidg0', 'rb+') as fd:
        fd.write(report.encode())

def keyboard_release():
    # Release keys
    write_report(NULL_CHAR*8)

def keyboard_do(letter, mod):
    write_report(mod + NULL_CHAR + chr(letter) + NULL_CHAR*5)
    sleep(0.05)
    keyboard_release()

def gpio_callback(channel):
    if GPIO.input(channel):     
        # Button-RELEASE / Switch:DOWN
        key_id, mod_id = gpio_button_map[channel][2], gpio_button_map[channel][3]
    else:                 
        # Button-PRESS / Switch:UP
        key_id, mod_id = gpio_button_map[channel][0], gpio_button_map[channel][1]

    if (key_id != KEY_NONE):
        print('Key:{} Mod:{}'.format(key_id, mod_id))
        keyboard_do(key_id, mod_id)


def main_key_loop():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM) 

    for k, v in gpio_button_map.items():
        GPIO.setup(k, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
        GPIO.add_event_detect(k ,GPIO.BOTH,callback=gpio_callback, bouncetime=200) 
    pause()

if __name__ == '__main__':
    try:
        main_key_loop()
    finally:
        keyboard_release()
        GPIO.cleanup()
