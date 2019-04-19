import keyboard, pyautogui,time, winshell, os
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
import pyttsx3
from win32api import GetKeyState
from win32con import VK_CAPITAL
import winshell, psutil


while True:
    # if keyboard.is_pressed(' '):
    #     print(pyautogui.position())
    #     time.sleep(1)

    time.sleep(300)
    pyautogui.press(' ')

# SPEECH_BOX = (39, 610, 60, 40)
# print(pyautogui.locateCenterOnScreen('speech_box.png', region=SPEECH_BOX))
#
# acc_f = open("account.txt", "r")
# acc_lines = acc_f.readlines()
# account_id = acc_lines[0][:-1]
# account_psd = acc_lines[1][:-1]
# log_in_data = [account_id, account_psd]
# bn_target = winshell.shortcut(os.path.join(winshell.desktop(), "暴雪战网.lnk")).path
#
# print(log_in_data)
# print(bn_target)

# image = 'test.jpg'
# img = Image.open('ocr_files\\' + image)
# img = PIL.ImageOps.invert(img)
# img.save('ocr_files\\' + '_con_' + image)
# img = cv2.imread('ocr_files\\' + '_con_' + image)
# img = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 3, 21)
# cv2.imwrite('ocr_files\\' + '_dnos_' + image, img)