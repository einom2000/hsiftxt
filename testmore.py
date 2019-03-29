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

def click_hb_btn(btn_name):
    time.sleep(0.3)
    pyautogui.moveTo(btn_name[0], btn_name[1], 0.5)
    time.sleep(0.2)
    pyautogui.click()


def kill_process(process_name, wd_name):
    for proc in psutil.process_iter():
        # check whether the process name matches
        if proc.name() == process_name:
            proc.kill()
            break
    while win32gui.FindWindow(None, wd_name):
        pass
    return


class LoginWindow:

    windowHwnd = 0

    def __init__(self, programdir, windowname, username, userpwd):
        self.programDir = programdir
        self.windowName = windowname
        self.userName = username
        self.userPwd = userpwd

    def runbnet(self):
        exist = win32gui.FindWindow(None, self.windowName)
        if exist == 0:
            win32api.WinExec(self.programDir)
        return

    def findWindow(self):
        while True:
            hwndbnt = win32gui.FindWindow(None, self.windowName)
            if hwndbnt == 0:
                continue
            else:
                win32gui.MoveWindow(hwndbnt, 100, 100, 365, 541, True)
            break
        win32gui.SetForegroundWindow(hwndbnt)
        time.sleep(0.5)
        return hwndbnt

    def login(self):
        # to log in id
        for i in range(4):  # orginal 4
            pyautogui.press('tab')
            time.sleep(random.randint(3, 5) / 10)
        # clear box
        pyautogui.press('backspace')
        time.sleep(random.randint(3, 5) / 10)
        # change to english
        pyautogui.press('shift')
        time.sleep(random.randint(3, 5) / 10)
        win32api.LoadKeyboardLayout('00000409', 1)
        time.sleep(random.randint(3, 5) / 10)
        # typein
        pyautogui.typewrite(self.userName, interval=(random.randint(15, 30) / 100))
        time.sleep((random.randint(15, 30) / 100))
        pyautogui.press('tab')
        pyautogui.typewrite(self.userPwd, interval=(random.randint(15, 30) / 100))
        time.sleep(5)
        for i in range(3):
            pyautogui.press('tab')
            time.sleep(random.randint(3, 5) / 10)
        # log in
        pyautogui.press('enter')
        return

def log_in(account):
    # open in battle net login window
    loginbt = LoginWindow(bn_target, '暴雪战网登录', account[0], account[1])
    logged_in = False
    logging_time = time.time()
    bt_window = 0
    while not logged_in:
        loginbt.runbnet()
        bn_hwnd = loginbt.findWindow()
        loginbt.login()
        # wait for the battle net window shows up
        time_login = time.time()
        while time.time() - time_login <= 50:
            bt_window = win32gui.FindWindow(None, '暴雪战网')
            if bt_window > 0:
                logged_in = True
                break
        if not logged_in:
            kill_process('Battle.net.exe', '暴雪战网登录')
        if time.time() - logging_time >= 600:
            # after 10 minutes failure, terminate program
            sys.exit()
    win32gui.SetForegroundWindow(bt_window)
    win32gui.MoveWindow(bt_window, 0, 0, 1280, 820, 1)
    bt_rec = win32gui.GetWindowRect(bt_window)
    time.sleep(1)

    while True:
        found = pyautogui.locateCenterOnScreen('bt_logged_in.png', region=(250, 650, 350, 200),
                                               grayscale=False, confidence=0.9)
        if found is not None:
            x = found[0]
            y = found[1]
            break
    pyautogui.moveTo(x, y, 1,  pyautogui.easeInQuad)
    pyautogui.click(x, y)

    # waiting for wow running
    wow_is_running = False
    wow_window = 0
    while not wow_is_running:
        wow_window = win32gui.FindWindow(None, '魔兽世界')
        if wow_window > 0:
            wow_is_running = True
    time.sleep(3)

CHANGE_ROLL = False
MAX_MONEY = 1000.00
UNIVERSIAL_DISCOUNT = 0.8
FISHOIL_MAX = 8000
CONFI = 0.9
ADJ = -2
LOGOUT_WOW_ICON = (49, 93, 40, 40)
SCAN_DONE_PIC = (300, 600 + ADJ, 110, 60)
CLOSE_TSM = (911, 128 + ADJ)
CLOSE_TSM_ICON = (897, 112, 40, 40)
RELOAD_SUCCESS = (1036, 709, 180, 50)
HISTORY_BUTTON_ON_SHOP = (641, 238 + ADJ)
BUY_SEARCH = (651, 161 + ADJ)
BUY_SEARCH_BACK = (217, 178 + ADJ)
ITEM_SEARCH = (863, 220 + ADJ)
SORT_RESULT = (867, 252 + ADJ)
FIRST_ROW_POST = (446, 267 + ADJ, 36, 14)
FIRST_ROW_STACK = (492, 267 + ADJ, 39, 14)
FIRST_ROW_BUYOUT = (815, 268 + ADJ, 89, 14)
FULL_SCAN_BUTTON = (343, 626 + ADJ)
INPUT_BOX = (377, 220 + ADJ)
BUYOUT_BUTTON_ON_SHOP = (799, 626 + ADJ)
AUCTION_BUTTON_ON_SHOP = (565, 626 + ADJ)
AUCTION_ON_SHOP_BIDING_PRICE_INPUT = (687, 431 + ADJ)
AUCTION_ON_SHOP_BUYOUT_PRICE_INPUT = (686, 453 + ADJ)
AUCTION_12_TIME = (590, 395 + ADJ)
AUCTION_ON_SHOP_STACK_INPUT = (683, 350 + ADJ)
AUCTION_ON_SHOP_POST_INPUT = (597, 350 + ADJ)
AUCTION_ON_SHOP_CONFIRM_BUTTON = (593, 500 + ADJ)
AUCTION_ON_SHOP_OK_BUTTON = (515, 610 + ADJ, 115, 40)
AUCTION_ON_SHOP_STOP_SCAN_BUTTON = (900, 638 + ADJ)
BUYOUT_ON_SHOP_OK_BUTTON = (735, 610 + ADJ, 115, 40)
ANTI_AFK = 480
SPEECH_BOX = (39, 610, 60, 40)
SCAN_ROW = 5
SELLER = (567, 60)  # x and length
SCAN_PERIOD = (350, 450)
END_TIME = [random.randint(2, 2), random.randint(10, 30)]
SECOND_ROLD_SELECTED = (1169, 152, 100, 50)
FOURTH_ROLD_SELECTED = (1169, 252, 100, 50)
BT_LOGGED_IN_REGION = (250, 650, 350, 200)
OFF_LINE_LOGO_REGION = (10, 30, 250, 150)
X_RATIO = 1.04
Y_RATIO = 1.04
J_RATIO = 1.85
Q_RATIO = 1.85
PORT = 'COM5'
DESKTOP = (2560, 1440)
acc_f = open("account.txt", "r")
acc_lines = acc_f.readlines()
account_id = acc_lines[0][:-1]
account_psd = acc_lines[1][:-1]
log_in_data = [account_id, account_psd]
bn_target = winshell.shortcut(os.path.join(winshell.desktop(), "暴雪战网.lnk")).path

kill_process('Wow.exe', '魔兽世界')
time.sleep(10)
log_in(log_in_data)
while pyautogui.locateCenterOnScreen('wow_icon.png', region=LOGOUT_WOW_ICON, confidence=CONFI) is None:
    pass

