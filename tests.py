import serial, keyboard, sys
import win32api, win32gui, winsound
import time, random, pyautogui
import logging, json
import cv2, os
from datetime import datetime
from tkinter import *
from PIL import Image, ImageFilter, ImageChops
import pytesseract
import numpy as np
import cv2
import PIL.ImageOps
import pyperclip
# from matplotlib import pyplot as plt
import json
import datetime

def key_2_sent(key):  # 'r' for right mouse double click, 'l' for left click, 't' for right click
    # 'o' for enter; 'u' for up; 'j' for down(jump); 'k' for space; '>' for ctrl-v, '<' for backspace
    # ']' for ctrl-a, '[' for ctrl-c, '?' is for ESC
    key_sent = str(key)
    ard.flush()
    # print("Python value sent: " + key_sent)
    ard.write(str.encode(key_sent))
    time.sleep(0.5)  # I shortened this to match the new value in your arduino code
    # waiting for pro micro to send 'Done'
    done_received = False
    while not done_received:
        original_msg = str(ard.read(ard.inWaiting()))  # read all characters in buffer
        # print(original_msg)
        # to git rid of the serial print additional letters.
        msg = original_msg.replace('b\'', '').replace('\\r\\n', "   ")[:-2]
        # print(msg[-4:])
        if msg[-4:] == 'Done':
            # print("Message from arduino: ")
            # print(msg)
            done_received = True
        else:
            ard.flush()
            time.sleep(0.5)
    return


PORT = 'COM17'
ard = serial.Serial(PORT, 9600, timeout=5)

while not keyboard.is_pressed(' '):
    pass
key_2_sent('?')
