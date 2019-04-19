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

# 1280*720

# This is for lower resolution other than 1280 x 720


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


def mouse_2_sent(position):
    key_sent = 'M' + str(int(position[0] / X_RATIO)) + ',' + str(int(position[1] / Y_RATIO))
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


def mouse_2_rtv(position):
    key_sent = 'N' + str(int(position[0] / J_RATIO)) + ',' + str(int(position[1] / Q_RATIO))
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


def get_random_wait(low, high):
    # wait for a random time
    time.sleep(random.randint(low * 1000, high * 1000) / 1000000)


def enumhandler(hwnd, lParam):
    # enumwindows' callback function
    # if found move to up_left corner
    if win32gui.IsWindowVisible(hwnd):
        if '魔兽世界' in win32gui.GetWindowText(hwnd):
            # rect = win32gui.GetWindowRect(hwnd)
            # print(rect[2] - rect[0], rect[3] - rect[1])
            win32gui.MoveWindow(hwnd, 0, 0, 1296, 759, True)
            # rect = win32gui.GetWindowRect(hwnd)
            # print(rect[2] - rect[0], rect[3] - rect[1])
            # print(rect)


def process_img(image):
    img = Image.open('ocr_files\\' + image)
    img = PIL.ImageOps.invert(img)
    img.save('ocr_files\\' + '_con_' + image)
    img = cv2.imread('ocr_files\\' + '_con_' + image)
    img = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 3, 21)
    # kernel = np.array([[-1, -1, -1], [-1, 9.6, -1], [-1, -1, -1]])
    # img = cv2.filter2D(img, -1, kernel)
    cv2.imwrite('ocr_files\\' + '_dnos_' + image, img)
    return img


class Item():
    def __init__(self):
        self.item_post = FIRST_ROW_POST
        self.item_stack = FIRST_ROW_STACK
        self.item_buyout = FIRST_ROW_BUYOUT

    def get(self, item_row, adjust):
        ####   post   ####
        pyautogui.screenshot('ocr_files\\' + str(item_row) + '_row_post.jpg',
                             region=(np.add(self.item_post, (0, item_row * 19 + adjust, 0, 0))))
        img = process_img(str(item_row) + '_row_post.jpg')
        # str_tmp = pytesseract.image_to_string(img, config='--psm 6')
        str_tmp = pytesseract.image_to_string(img, lang='eng',
                                              config='--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789')
        str_tmp = str_tmp.replace('l', '1')
        str_tmp = str_tmp.replace('g', '9')
        str_tmp = str_tmp.replace('°', '')
        str_tmp = str_tmp.replace('s', '5')
        str_tmp = str_tmp.replace('B', '8')
        total_tmp = str_tmp
        try:
            post_num = int(re.findall("\d+", str_tmp)[0])
        except ValueError:
            post_num = 1
        except IndexError:
            post_num = 1
        ####   stack   ####
        pyautogui.screenshot('ocr_files\\' + str(item_row) + '_row_stack.jpg',
                             region=(np.add(self.item_stack, (0, item_row * 19 + adjust, 0, 0))))
        img = process_img(str(item_row) + '_row_stack.jpg')
        str_tmp = pytesseract.image_to_string(img, config='--psm 6')
        str_tmp = str_tmp.replace('l', '1')
        str_tmp = str_tmp.replace('g', '9')
        str_tmp = str_tmp.replace('s', '5')
        str_tmp = str_tmp.replace('S', '5')
        str_tmp = str_tmp[:3]
        total_tmp = total_tmp + ' | ' + str_tmp
        try:
            stack_num = int(re.findall("\d+", str_tmp)[0])
        except IndexError:
            stack_num = 0
        ####   buyout   ####
        pyautogui.screenshot('ocr_files\\' + str(item_row) + '_row_buyout.jpg',
                             region=(np.add(self.item_buyout, (0, item_row * 19 + adjust, 0, 0))))
        img = process_img(str(item_row) + '_row_buyout.jpg')
        str_tmp = pytesseract.image_to_string(img, config='--psm 6')
        str_tmp = str_tmp.replace('l', '1')
        str_tmp = str_tmp.replace(' ', '')
        str_tmp = str_tmp.replace('q', 'g')
        if 'g' in str_tmp:
            lst = list(str_tmp)
            lst[-4] = 's'
            lst[-1] = 'c'
            str_tmp = ''.join(lst)
        # print(str_tmp)
        total_tmp = total_tmp + ' | ' + str_tmp
        if 'g' in str_tmp and 's' in str_tmp and 'c' in str_tmp:
            str_tmp_gold = str_tmp[:str_tmp.index('g')]
            str_tmp_svr = str_tmp[str_tmp.index('g') + 1: str_tmp.index('s')]
            str_tmp_cpp = str_tmp[str_tmp.index('s') + 1: -1]
            try:
                gold = int(re.findall("\d+", str_tmp_gold)[0])
            except IndexError:
                gold = 0
            try:
                silver = int(re.findall("\d+", str_tmp_svr)[0])
            except IndexError:
                silver = 0
            try:
                copper = int(re.findall("\d+", str_tmp_cpp)[0])
            except IndexError:
                copper = 0
        elif 's' in str_tmp and 'c' in str_tmp:
            str_tmp_svr = str_tmp[: str_tmp.index('s')]
            str_tmp_cpp = str_tmp[str_tmp.index('s') + 1: -1]
            gold = 0
            try:
                silver = int(re.findall("\d+", str_tmp_svr)[0])
            except IndexError:
                silver = 0
            try:
                copper = int(re.findall("\d+", str_tmp_cpp)[0])
            except IndexError:
                copper = 0
        else:
            gold, silver, copper = 0, 0, 0
        buyout_price = copper + silver * 100 + gold * 10000
        print(total_tmp)
        return post_num, stack_num, buyout_price


def move2(tar_position):
    cur_position = pyautogui.position()
    rlt_x = tar_position[0] - cur_position[0]
    rlt_y = tar_position[1] - cur_position[1]
    while abs(rlt_x) > 2 or abs(rlt_y) > 2:
        if abs(rlt_x) > 175:
            rlt_x = 175 * (rlt_x / abs(rlt_x))
        if abs(rlt_y) > 175:
            rlt_y = 175 * (rlt_y / abs(rlt_y))
        mouse_2_rtv([rlt_x, rlt_y])
        # print('relative move: ' + str([rlt_x, rlt_y]))
        cur_position = pyautogui.position()
        rlt_x = tar_position[0] - cur_position[0]
        rlt_y = tar_position[1] - cur_position[1]


def open_tsm():
    t = time.time()
    while True:
        key_2_sent('g')
        get_random_wait(300, 700)
        key_2_sent('y')
        get_random_wait(500, 700)
        fd = pyautogui.locateCenterOnScreen('close_tsm_icon.png', region=CLOSE_TSM_ICON)
        if fd is not None:
            break
        if time.time() - t >= 4:
            key_2_sent('h')
            while pyautogui.locateCenterOnScreen('reload_success.png', region=RELOAD_SUCCESS) is None:
                pass
            t = time.time()
    action_list = [BUY_SEARCH, HISTORY_BUTTON_ON_SHOP]
    for act in action_list:
        move2(act)
        key_2_sent('l')
    scan_is_end('000')


def close_tsm():
    move2(CLOSE_TSM)
    key_2_sent('l')
    get_random_wait(1200, 1500)
    pass


def is_off_line():
    start_t = time.time()
    found = None
    while time.time() - start_t <= 60:
        found = pyautogui.locateCenterOnScreen('off_line_logo.png', region=OFF_LINE_LOGO_REGION,
                                               grayscale=False, confidence=0.9)
        if found is not None:
            break
    return found


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
        found = pyautogui.locateCenterOnScreen('bt_logged_in.png', region=BT_LOGGED_IN_REGION,
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

    time.sleep(20)
    win32gui.EnumWindows(enumhandler, None)


def select_all_and_paste():
    get_random_wait(100, 200)
    key_2_sent('l')
    get_random_wait(100, 200)
    key_2_sent(']')   # ctrl-a
    get_random_wait(100, 200)
    key_2_sent(']')
    get_random_wait(300, 500)
    key_2_sent('>')   # ctrl-v
    get_random_wait(100, 200)
    key_2_sent('o')   # enter
    get_random_wait(100, 200)

def scan_is_end(scaned_name):
    found = False
    ct = time.time()
    tried = 0
    while not found:
        fd = pyautogui.locateCenterOnScreen('scan_done.png', region=SCAN_DONE_PIC, grayscale=False)
        if fd is not None:
            found = True
            time.sleep(1)
            engine.say('扫描完成')
            engine.runAndWait()
            break
        time.sleep(0.5)
        print('wating for scan to finish, rescan after' + str(int(60 - time.time() + ct)))
        # engine.say('等待扫描结束, 或在' + str(int(60 - time.time() + ct)) + '秒后重新扫描')
        # engine.runAndWait()
        if time.time() - ct >= 60 and tried < 2:
            if pyautogui.locateCenterOnScreen('speech_box.png', region=SPEECH_BOX) is not None:
                key_2_sent('?')
                get_random_wait(1100, 1200)
            move2(AUCTION_ON_SHOP_STOP_SCAN_BUTTON)
            key_2_sent('l')
            get_random_wait(1100, 1200)
            move2(INPUT_BOX)
            select_all_and_paste()
            get_random_wait(1100, 1200)
            # key_2_sent('k')  # jump
            tried += 1
            ct = time.time()
        elif tried >= 2:
            close_tsm()
            if is_off_line() is not None:
                kill_process('Wow.exe', '魔兽世界')
                time.sleep(10)
                log_in(log_in_data)
                while pyautogui.locateCenterOnScreen('role_select_icon.png', region=ROLE_SELECT_ICON_REGION,
                                                     confidence=CONFI) is None:
                    pass
                get_random_wait(1200, 1500)
                key_2_sent('o')
                while pyautogui.locateCenterOnScreen('reload_success.png', region=RELOAD_SUCCESS,
                                                     confidence=CONFI) is None:
                    get_random_wait(20000, 30000)
                    key_2_sent('o')
                    pass

            elif pyautogui.locateCenterOnScreen('wow_icon.png', region=LOGOUT_WOW_ICON, confidence=CONFI) is not None:
                get_random_wait(1200, 1500)
                key_2_sent('o')
                while pyautogui.locateCenterOnScreen('reload_success.png', region=RELOAD_SUCCESS, confidence=CONFI) \
                       is None:
                    get_random_wait(20000, 30000)
                    key_2_sent('o')
                    pass
            key_2_sent('k')  # jump
            open_tsm()
            if scaned_name != '000':
                input_box(INPUT_BOX, scaned_name + '/exact')
            tried = 0


def input_box(positon, scr):
    move2(positon)
    get_random_wait(100, 200)
    key_2_sent('l')
    get_random_wait(100, 200)
    key_2_sent(']')
    get_random_wait(100, 200)
    key_2_sent(']')
    get_random_wait(100, 200)
    pyperclip.copy(scr)
    key_2_sent('>')
    get_random_wait(100, 200)
    key_2_sent('o')
    get_random_wait(100, 200)


def anti_afk():
    global t
    if time.time() - t >= ANTI_AFK:
        key_2_sent('k')
        get_random_wait(1000, 2000)
        t = time.time()
        # key_2_sent('h')
        # while pyautogui.locateCenterOnScreen('reload_success.png', region=RELOAD_SUCCESS) is None:
        #     pass
        # close_tsm()
        # open_tsm()
        # action_list = [BUY_SEARCH, HISTORY_BUTTON_ON_SHOP]
        # for act in action_list:
        #     move2(act)
        #     key_2_sent('l')
        # logging.info('wow reloaded, tsm opened')
        # scan_is_end('000')


while GetKeyState(VK_CAPITAL):
    pyautogui.press('capslock')


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

# ======CONSTANTS========
'''
G  == target npc
Y  == talk with npc
H  == /RL MACRO
- == /LOGOUT /MACRO
SET ENTER TO ELSE THAN CHAT
'''
# full screen size 1280x720
# minimize the aution panel to the topleft of the top action bar
'''
(911, 128) close button of top right
(641, 161) auction buy search button
(217, 178) auction buy search button backspace
(863, 220) auction item search
(867, 250) auction search sort
(446, 267) (482, 280) first row posts
(492, 267) (531, 280) first row stack/post
(320, 614)(403, 650) scan_done
(321, 617) BUY_SCAN_BUTTON
(277, 220) INPUT_BOX
'''
SNIPPER_OVER_SCAN = 3
THEME = 'daytime'
ONLY_RECORD = False
CHANGE_ROLL = False
MAX_MONEY = 3000.00
UNIVERSIAL_DISCOUNT = 1
FISHOIL_MAX = 8000
CONFI = 0.9
ADJ = -1
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
END_TIME = [random.randint(4, 6), random.randint(10, 30)]
SECOND_ROLD_SELECTED = (1169, 152, 100, 50)
FOURTH_ROLD_SELECTED = (1169, 252, 100, 50)
BT_LOGGED_IN_REGION = (250, 650, 350, 200)
OFF_LINE_LOGO_REGION = (10, 30, 250, 150)
ROLE_SELECT_ICON_REGION = (550, 650, 250, 100)
X_RATIO = 1.04
Y_RATIO = 1.04
J_RATIO = 1.85
Q_RATIO = 1.85
PORT = 'COM5'
DESKTOP = (2560, 1440)  # Related with X_RATIO, and Y_RATIO, set in arduino manually


# ======= json file structure for scan_data.json ======
'''
in file target_goods_list.json
[
    ['锚草', '阿昆达之噬', '凛冬之吻', '海潮茎杆', '流波花苞', '海妖花粉', '星光苔'],
    {                                '锚草': [0, 99999, 100, 9000, 0, 3, 100],
                                     '阿昆达之噬': [0, 99999, 100, 8000, 0, 3, 100],
                                     '凛冬之吻': [0, 99999, 100, 1200, 0, 3, 100],
                                     '海潮茎杆': [0, 99999, 100, 1000, 0, 3, 100],
                                     '流波花苞': [0, 99999, 100, 2000, 0, 3, 100],
                                     '海妖花粉': [0, 99999, 100, 2000, 0, 3, 100],
                                     '星光苔': [0, 99999, 100, 1000, 0, 3, 100]
    },

]

'''

'''
in file scan_data.json

{
'item_name':'锚草', 
'item_onshelf_lowest': 999999,
'item_onshelf_sticking_volume': 100,
'item_threshold_price': 9000, 
'item_threshold_pct': 7 / 100,
'item_onshelf_post': 3,
'item_onshelf_stack': 100,
'item_buyout_history':[{
                            'date&time': '',
,                           'threshold_price':99999999,
                            'threshold_pct': 0,
                            'buyout_price':0,
                            'buyout_stack':0,
                            'buyout_post':0,
                            '2nd_quotes':0
                        },
                        {
                            'date&time': '',
                            'threshold_price':99999999,
                            'threshold_pct': 0,
                            'buyout_price':0,
                            'buyout_stack':0,
                            'buyout_post':0,
                            '2nd_quotes':0
                        }], 
'item_onshelf_history':[{
                            'date&time':'',
                            'sticking_volume':0,
                            'sticking_volume's price':0,
                            'onshelf_price':0,
                            'onshelf_volume':0,
                            'is_onshelf':'True'               
                        },
                        {
                            'date&time':'',
                            'sticking_volume':0,
                            'sticking_volume's price':0,
                            'onshelf_price':0,
                            'onshelf_volume':0,
                            'is_onshelf':'True'
                        }]
'''

'''
in file '../scan_history/____history.json:

[{                          'date&time':'',
                            '1st_quote_post':0,
                            '1st_quote_stack':0,
                            '1st_quote_buyout':0,
                            '2nd_quote_post':0,
                            '2nd_quote_stack':0,
                            '2nd_quote_buyout':0,
                            '3rd_quote_post':0,
                            '3rd_quote_stack':0,
                            '3rd_quote_buyout':0,
                        },
                        {
                            'date&time':'',
                            '1st_quote_post':0,
                            '1st_quote_stack':0,
                            '1st_quote_buyout':0,
                            '2nd_quote_post':0,
                            '2nd_quote_stack':0,
                            '2nd_quote_buyout':0,
                            '3rd_quote_post':0,
                            '3rd_quote_stack':0,
                            '3rd_quote_buyout':0
                        }]

'''

# -------------------data file initialization-------------------------------------
time.sleep(5)
with open('target_goods_list.json', 'r') as fp:
    target_goods_list = json.load(fp)
    all_goods_names = target_goods_list[0]  # the botting goods name list
    all_goods_to_do = target_goods_list[1]
    # [on_shelf?, threshold_on_shelf_price(lowest), sticking_volume, snip_threshold_price(highest),
    #  ship_threshold_price_percentage(first 3 rows)]

# ===== loading history and initializing data to check any new items=====
with open('scan_data.json', 'r') as fp:
    scan_data = json.load(fp)


for item in all_goods_names:
    recorded = False
    for recorded_item in scan_data:
        if recorded_item.get('item_name') == item:
            recorded = True
            print(item + 'recorded')
    if not recorded:
        print(item + 'NOT recorded')
        scan_data.append({
            'item_name': item,
            'item_onshelf_lowest': all_goods_to_do.get(item)[1],
            'item_onshelf_sticking_volume': all_goods_to_do.get(item)[2],
            'item_threshold_price': all_goods_to_do.get(item)[3],
            'item_threshold_pct': all_goods_to_do.get(item)[4],
            'item_onshelf_post': all_goods_to_do.get(item)[5],
            'item_onshelf_stack': all_goods_to_do.get(item)[6],
            'item_buyout_history': [],
            'item_onshelf_history': []
        })
        with open('scan_history\\' + item + '_history.json', 'w') as fp:
            json.dump([], fp, ensure_ascii=False)
with open('scan_data.json', 'w') as fp:
    json.dump(scan_data, fp, ensure_ascii=False)

acc_f = open("account.txt", "r")
acc_lines = acc_f.readlines()
account_id = acc_lines[0][:-1]
account_psd = acc_lines[1][:-1]
log_in_data = [account_id, account_psd]
bn_target = winshell.shortcut(os.path.join(winshell.desktop(), "暴雪战网.lnk")).path

# =======INITIALIZATION========
logging.basicConfig(filename='AUCTION_LOGGING.log',
                    filemode='w',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG
                    )

ard = serial.Serial(PORT, 9600, timeout=5)
time.sleep(2)
logging.info('Serial opened and program starts!')

win32gui.EnumWindows(enumhandler, None)

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
engine = pyttsx3.init()

# ===== wait to start ====
print('press F10 to start..')
engine.say('请按F十开始,或者F九纪录数据')
engine.runAndWait()
while not keyboard.is_pressed('F10'):
    if keyboard.is_pressed('F9'):
        ONLY_RECORD = True
        break
    pass
engine.say('程序开始')
engine.runAndWait()

# ====== start tsm ========
t = time.time()

logging.info('ready to start, tsm opened')

fish_oil_count = 0

open_tsm()

snipper_over_scan = 0

while True:

    # timetable for fishing during a day
    if 18 > datetime.datetime.now().hour >= 12:
        TIME_TO_RUN = random.randint(12, 18)
        SCAN_ROW = 4
        SCAN_PERIOD = (40, 60)
        THEME = 'afternoon'
    elif datetime.datetime.now().hour >= 18:
        TIME_TO_RUN = random.randint(9, 12)
        SCAN_ROW = 4
        SCAN_PERIOD = (40, 60)
        THEME = 'night'
    elif datetime.datetime.now().hour <= 3:
        TIME_TO_RUN = random.randint(9, 12)
        SCAN_ROW = 4
        SCAN_PERIOD = (40, 60)
        THEME = 'night'
    else:
        TIME_TO_RUN = random.randint(18, 20)
        SCAN_ROW = 4
        SCAN_PERIOD = (40, 60)
        THEME = 'daytime'
    # force to end
    print('Now is ' + str(datetime.datetime.now().hour) + '. Program is going to terminate on ' +
          str(END_TIME[0]) + ':' + str(END_TIME[1]) + ' .')
    # engine.say('现在是 ' + str(datetime.datetime.now().hour) + '. 程序将结束于 ' +
    #            str(END_TIME[0]) + ':' + str(END_TIME[1]) + ' .')
    # engine.runAndWait()
    print('Fishing duration currently is ' + str(TIME_TO_RUN * 0) + ' minutes.')

    if datetime.datetime.now().hour == END_TIME[0] and datetime.datetime.now().minute >= END_TIME[1]:
        sys.exit()
    # anti AFK
    anti_afk()
    for goods_name in all_goods_names:
        # anti AFK
        anti_afk()

        if ((all_goods_to_do.get(goods_name)[0] == 2 and THEME == 'daytime')
                and all_goods_to_do.get(goods_name)[0] != 9) \
                or all_goods_to_do.get(goods_name)[0] == 0 \
                or all_goods_to_do.get(goods_name)[0] == 1 \
                or (all_goods_to_do.get(goods_name)[0] == 2 and THEME != 'daytime'
                    and snipper_over_scan % 4 == 0
                    and all_goods_to_do.get(goods_name)[0] != 9):


            # engine.say('扫描 ' + goods_name)
            # engine.runAndWait()

            input_box(INPUT_BOX, goods_name + '/exact')

            goods = Item()


            scan_is_end(goods_name)

            # move2(SORT_RESULT)
            # key_2_sent('l')
            # get_random_wait(500, 1000)

            quotes = []

            for i in range(SCAN_ROW):
                quote = goods.get(i, 0)
                if quote[2] == 0:
                    time.sleep(2)
                    engine.say('扫描的零价格，重新识别一次')
                    engine.runAndWait()
                    quote = goods.get(i, 0)
                quotes.append(quote)
                print(quote)
            with open('scan_history\\' + goods_name + '_history.json', 'r') as fp:
                data = json.load(fp)
            data.append({'date&time': datetime.datetime.today().strftime('%Y-%m-%d %H:%M')
                                      + ' (' + datetime.datetime.today().strftime('%A'),
                         '1st_quote_post': quotes[0][0],
                         '1st_quote_stack': quotes[0][1],
                         '1st_quote_buyout': quotes[0][2],
                         '2nd_quote_post': quotes[1][0],
                         '2nd_quote_stack': quotes[1][1],
                         '2nd_quote_buyout': quotes[1][2],
                         '3rd_quote_post': quotes[2][0],
                         '3rd_quote_stack': quotes[2][1],
                         '3rd_quote_buyout': quotes[2][2],
                         })
            with open('scan_history\\' + goods_name + '_history.json', 'w') as fp:
                json.dump(data, fp, ensure_ascii=False)
            # goods name = 'ABC'
            # goods_to_do ={"暗月火酒": [1, 13000, 5, 9000, 7, 1, 1]}
            # quotes

            # to check if the goods is the on_shelf goods:
            on_shelf = all_goods_to_do.get(goods_name)[0]
            if on_shelf == 1:
                on_shelf_lowest = all_goods_to_do.get(goods_name)[1]
                on_shelf_sticking_volume = all_goods_to_do.get(goods_name)[2]
                on_shelf_post = all_goods_to_do.get(goods_name)[5] - random.randint(0, 1)
                on_shelf_post = all_goods_to_do.get(goods_name)[5] - random.randint(0, 1)
                on_shelf_stack = all_goods_to_do.get(goods_name)[6]
                if 180 > on_shelf_stack >= 100:
                    on_shelf_stack = random.randint(int(all_goods_to_do.get(goods_name)[6] / 20) - 0,
                                                    int(all_goods_to_do.get(goods_name)[6] / 20) + 0) * 20
                quit_on_shelf = 0
                for i in range(SCAN_ROW):
                    try:
                        if quotes[i][1] * quotes[i][0] > int(1 * on_shelf_sticking_volume):  # and quotes[i][1] * quotes[i][0] <= 120:
                        # if quotes[i][1] == 5 or quotes[i][1] == 20:
                            fd = pyautogui.locateCenterOnScreen('self.png', region=
                                            (SELLER[0] - 10, FIRST_ROW_POST[1] + 0 * i * 19, SELLER[1] + 10,
                                             (i + 1) * 19 + ADJ), confidence=CONFI)

                            im = pyautogui.screenshot(region=
                                            (SELLER[0] - 10, FIRST_ROW_POST[1] + 0 * i * 19, SELLER[1] + 10,
                                             (i + 1) * 19 + ADJ))
                            im.save('temp_sc.png')
                            engine.say('上架货物价格分析中')
                            engine.runAndWait()
                            fd2 = pyautogui.locateCenterOnScreen('self2.png', region=
                                            (SELLER[0] - 10, FIRST_ROW_POST[1] + 0 * i * 19, SELLER[1] + 10,
                                             FIRST_ROW_POST[3] * (i + 1) + 10), confidence=CONFI)
                            print(fd, fd2)
                            if fd is None and fd2 is None and quotes[i][2] >= on_shelf_lowest * 100:
                                print((SELLER[0], FIRST_ROW_POST[1] + i * 19 + 5))
                                engine.say('竞争牌价到前位')
                                engine.runAndWait()
                                move2((SELLER[0], FIRST_ROW_POST[1] + i * 19 + 5))
                                key_2_sent('l')
                                get_random_wait(300, 600)
                                if pyautogui.locateCenterOnScreen('list_auction_ok.png',
                                                                  region=AUCTION_ON_SHOP_OK_BUTTON) is not None:
                                    move2(AUCTION_BUTTON_ON_SHOP)
                                    key_2_sent('l')
                                    input_box(AUCTION_ON_SHOP_STACK_INPUT, on_shelf_stack)
                                    input_box(AUCTION_ON_SHOP_POST_INPUT, on_shelf_post)  #  1 * int(quotes[i][0] )
                                    move2(AUCTION_12_TIME)
                                    key_2_sent('l')
                                    move2(AUCTION_ON_SHOP_BUYOUT_PRICE_INPUT)
                                    key_2_sent('l')
                                    get_random_wait(100, 300)
                                    key_2_sent('[')
                                    get_random_wait(100, 300)
                                    biding_price = pyperclip.paste()
                                    input_box(AUCTION_ON_SHOP_BIDING_PRICE_INPUT, biding_price)
                                    move2(AUCTION_ON_SHOP_CONFIRM_BUTTON)
                                    get_random_wait(100, 300)
                                    key_2_sent('l')
                                    # record
                                    with open('scan_data.json', 'r') as fp:
                                        scan_data = json.load(fp)
                                    for record in scan_data:
                                        if record.get('item_name') == goods_name:
                                            on_shelf_record = {
                                                'date&time': datetime.datetime.today().strftime('%Y-%m-%d %H:%M')
                                                             + ' (' + datetime.datetime.today().strftime('%A'),
                                                'sticking_volume': on_shelf_sticking_volume,
                                                'sticking_volume price': quotes[i][2],
                                                'onshelf_price': biding_price,
                                                'onshelf_volume': on_shelf_stack * on_shelf_post,
                                                'is_onshelf': 'True'
                                            }
                                            record.get('item_onshelf_history').append(on_shelf_record)
                                            with open('scan_data.json', 'w') as fp:
                                                json.dump(scan_data, fp, ensure_ascii=False)
                                            break
                                # special for the '暗月火酒'
                                elif goods_name == '暗月火酒' and pyautogui.locateCenterOnScreen('list_auction_ok.png',
                                                                  region=AUCTION_ON_SHOP_OK_BUTTON) is None:
                                    move2((SELLER[0], FIRST_ROW_POST[1] + (i + 1) * 19 + 5))
                                    key_2_sent('l')
                                    get_random_wait(300, 600)
                                    move2(AUCTION_BUTTON_ON_SHOP)
                                    key_2_sent('l')
                                    input_box(AUCTION_ON_SHOP_STACK_INPUT, on_shelf_stack)
                                    input_box(AUCTION_ON_SHOP_POST_INPUT, on_shelf_post)  #  1 * int(quotes[i][0] )
                                    move2(AUCTION_12_TIME)
                                    key_2_sent('l')
                                    move2(AUCTION_ON_SHOP_BUYOUT_PRICE_INPUT)
                                    key_2_sent('l')
                                    get_random_wait(100, 300)
                                    key_2_sent('[')
                                    get_random_wait(100, 300)
                                    biding_price = pyperclip.paste()
                                    input_box(AUCTION_ON_SHOP_BIDING_PRICE_INPUT, biding_price)
                                    move2(AUCTION_ON_SHOP_CONFIRM_BUTTON)
                                    get_random_wait(100, 300)
                                    key_2_sent('l')
                                    # record
                                    with open('scan_data.json', 'r') as fp:
                                        scan_data = json.load(fp)
                                    for record in scan_data:
                                        if record.get('item_name') == goods_name:
                                            on_shelf_record = {
                                                'date&time': datetime.datetime.today().strftime('%Y-%m-%d %H:%M')
                                                             + ' (' + datetime.datetime.today().strftime('%A'),
                                                'sticking_volume': on_shelf_sticking_volume,
                                                'sticking_volume price': quotes[i][2],
                                                'onshelf_price': biding_price,
                                                'onshelf_volume': on_shelf_stack * on_shelf_post,
                                                'is_onshelf': 'True'
                                            }
                                            record.get('item_onshelf_history').append(on_shelf_record)
                                            with open('scan_data.json', 'w') as fp:
                                                json.dump(scan_data, fp, ensure_ascii=False)
                                            break
                                quit_on_shelf = 1
                            if fd is not None or fd2 is not None:
                                quit_on_shelf = 1
                    except IndexError:
                        break

                    if quit_on_shelf == 1:
                        break
            if on_shelf < 3 or ONLY_RECORD is True: # 0, and 1 all to buy lowest, 2 to just scanner
                threshold_price = all_goods_to_do.get(goods_name)[3] * 100 * UNIVERSIAL_DISCOUNT
                print('threshold_price = ' + str(threshold_price))
                triger_pct = all_goods_to_do.get(goods_name)[4] / 100
                print(triger_pct)
                if triger_pct >= 0.7:
                    triger_pct = 0.7
                second_quote = quotes[1][2]
                if quotes[1][2] == 0:
                    second_quote = quotes[0][2] + 1
                print(quotes[0][2] / second_quote)
                print(quotes[0][2], threshold_price )
                print(quotes[0][2] * quotes[0][1], MAX_MONEY )
                if (quotes[0][2] != 0 and quotes[1][2] != 0 and quotes[0][2] / second_quote <= triger_pct) or \
                        (quotes[0][2] <= threshold_price and quotes[0][2] * quotes[0][1] / 10000 <= MAX_MONEY ) or \
                        ONLY_RECORD is True or on_shelf == 2:

                    if ONLY_RECORD is not True and on_shelf != 2 and quotes[0][2] != 0:
                        move2((FIRST_ROW_POST[0], FIRST_ROW_POST[1] + 9))
                        engine.say('找到低价格，准备买入')
                        engine.runAndWait()
                        get_random_wait(100, 300)
                        key_2_sent('l')
                        get_random_wait(100, 300)
                        move2(BUYOUT_BUTTON_ON_SHOP)
                        for i in range(1):
                            key_2_sent('l')
                            get_random_wait(500, 1000)
                engine.say('价格纪录在案')
                engine.runAndWait()
                with open('scan_data.json', 'r') as fp:
                    scan_data = json.load(fp)
                for record in scan_data:
                    if record.get('item_name') == goods_name:
                        buy_out_record = {
                            'date&time': datetime.datetime.today().strftime('%Y-%m-%d %H:%M')
                                         + ' (' + datetime.datetime.today().strftime('%A'),
                            'threshold_price': threshold_price / 100,
                            'threshold_pct': triger_pct,
                            'buyout_price': quotes[0][2],
                            'buyout_post': quotes[0][0],
                            'buyout_stack': quotes[0][1],
                            '2nd_quotes': quotes[1][2]
                        }
                        record.get('item_buyout_history').append(buy_out_record)
                        with open('scan_data.json', 'w') as fp:
                            json.dump(scan_data, fp, ensure_ascii=False)
                        break

            # else to check if the 1st is lower the threshold of snipper
            # to check if the 1st is lower than % of the threshold
            # to check if the price is lower than % of the second
            # if yes ,buyout and record

    t1 = time.time()
    wait = random.randint(SCAN_PERIOD[0], SCAN_PERIOD[1])
    while time.time() - t1 <= wait:
        print('change role and rescan after ' + str(int(wait - (time.time() - t1))) + ' seconds.')
        engine.say('在 ' + str(int(wait - (time.time() - t1))) + ' 更换角色或重新循环任务')
        engine.runAndWait()
        if fish_oil_count < FISHOIL_MAX:
            get_random_wait(15000, 20000)
            key_2_sent('f')
        else:
            get_random_wait(200, 400)
        print('Now is ' + str(datetime.datetime.now().hour) + '. Program is going to terminate on ' +
              str(END_TIME[0]) + ':' + str(END_TIME[1]) + ' .')
        # engine.say('现在是 ' + str(datetime.datetime.now().hour) + '. 程序将结束于 ' +
        #       str(END_TIME[0]) + ':' + str(END_TIME[1]) + ' .')
        # engine.runAndWait()

    if datetime.datetime.now().hour == END_TIME[0] and datetime.datetime.now().minute >= END_TIME[1]:
        sys.exit()

    if CHANGE_ROLL:
        key_2_sent('-')
        while pyautogui.locateCenterOnScreen('wow_icon.png', region=LOGOUT_WOW_ICON, confidence=CONFI) is None:
            pass
        get_random_wait(1200, 1500)
        key_2_sent('u')
        get_random_wait(1200, 1500)
        key_2_sent('o')
        while pyautogui.locateCenterOnScreen('reload_success.png', region=RELOAD_SUCCESS, confidence=CONFI) is None:
            get_random_wait(20000, 30000)
            key_2_sent('o')
            pass

    snipper_over_scan += 1

