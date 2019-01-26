import serial, keyboard, sys
import win32api, win32gui, winsound
import time, random, pyautogui
import logging, json
import cv2, os
from datetime import datetime


logging.basicConfig(filename='leveling.log',
                    filemode='w',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG
                    )
logging.info('Program starts!')

X_RATIO = 1
Y_RATIO = 1

def key_2_sent(key):
    key_sent = str(key)
    ard.flush()
    print ("Python value sent: " + key_sent)
    ard.write(str.encode(key_sent))
    time.sleep(0.5) # I shortened this to match the new value in your arduino code
    # waiting for pro micro to send 'Done'
    done_received = False
    while not done_received:
        original_msg = str(ard.read(ard.inWaiting())) # read all characters in buffer
        # print(original_msg)
        # to git rid of the serial print additional letters.
        msg = original_msg.replace('b\'', '').replace('\\r\\n', "   ")[:-2]
        # print(msg[-4:])
        if msg[-4:] == 'Done':
            print("Message from arduino: ")
            print(msg)
            done_received = True
        else:
            ard.flush()
            time.sleep(0.5)
    return

def mouse_2_sent(position):
    key_sent = 'M' + str(int(position[0] / X_RATIO)) + ',' + str(int(position[1] / Y_RATIO))
    ard.flush()
    print ("Python value sent: " + key_sent)
    ard.write(str.encode(key_sent))
    time.sleep(0.5) # I shortened this to match the new value in your arduino code
    # waiting for pro micro to send 'Done'
    done_received = False
    while not done_received:
        original_msg = str(ard.read(ard.inWaiting())) # read all characters in buffer
        # print(original_msg)
        # to git rid of the serial print additional letters.
        msg = original_msg.replace('b\'', '').replace('\\r\\n', "   ")[:-2]
        # print(msg[-4:])
        if msg[-4:] == 'Done':
            print("Message from arduino: ")
            print(msg)
            done_received = True
        else:
            ard.flush()
            time.sleep(0.5)
    return

port = 'COM17'
ard = serial.Serial(port, 9600, timeout=5)
time.sleep(2)  # wait for arduino

#
# mouse_2_sent([100,100])
# print(pyautogui.position())
# time.sleep(3)
# mouse_2_sent([2560, 1440])
# print(pyautogui.position())
mouse_2_sent([300, 200])
print('000')
i = 0

key_2_sent('l')
print('11')
i = 1