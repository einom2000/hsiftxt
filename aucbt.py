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
    time.sleep(random.randint(low, high) / 1000)


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
    img = Image.open(image)
    img = PIL.ImageOps.invert(img)
    img.save('_con_' + image)
    img = cv2.imread('_con_' + image)
    img = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 3, 21)
    cv2.imwrite('_dnos_' + image, img)
    return img



class Item():
    def __init__(self):
        self.item_post = FIRST_ROW_POST
        self.item_stack = FIRST_ROW_STACK
        self.item_buyout = FIRST_ROW_BUYOUT

    def get(self, item_row , adjust):
        ####   post   ####
        pyautogui.screenshot(str(item_row)+'_row_post.jpg',
                             region=(np.add(self.item_post, (0, item_row * 19 + adjust, 0, 0))))
        img = process_img(str(item_row)+'_row_post.jpg')
        # str_tmp = pytesseract.image_to_string(img, config='--psm 6')
        str_tmp = pytesseract.image_to_string(img, lang='eng',
                                              config='--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789')
        str_tmp = str_tmp.replace('l', '1')
        str_tmp = str_tmp.replace('g', '9')
        str_tmp = str_tmp.replace('°', '')
        str_tmp = str_tmp.replace('s', '5')
        str_tmp = str_tmp.replace('S', '5')
        total_tmp = str_tmp
        try:
            post_num = int(re.findall("\d+", str_tmp)[0])
        except ValueError:
            post_num = 0
        ####   stack   ####
        pyautogui.screenshot(str(item_row)+'_row_stack.jpg',
                             region=(np.add(self.item_stack, (0, item_row * 19 + adjust, 0, 0))))
        img = process_img(str(item_row)+'_row_stack.jpg')
        str_tmp = pytesseract.image_to_string(img, config='--psm 6')
        str_tmp = str_tmp.replace('l', '1')
        str_tmp = str_tmp.replace('g', '9')
        str_tmp = str_tmp.replace('s', '5')
        str_tmp = str_tmp.replace('S', '5')
        str_tmp = str_tmp[:3]
        total_tmp = total_tmp + ' | ' + str_tmp
        try:
            stack_num = int(re.findall("\d+", str_tmp)[0])
        except ValueError:
            stack_num = 0
        ####   buyout   ####
        pyautogui.screenshot(str(item_row)+'_row_buyout.jpg',
                             region=(np.add(self.item_buyout, (0, item_row * 19 + adjust, 0, 0))))
        img = process_img(str(item_row)+'_row_buyout.jpg')
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
            except ValueError:
                gold = 0
            try:
                silver = int(re.findall("\d+", str_tmp_svr)[0])
            except ValueError:
                silver = 0
            try:
                copper = int(re.findall("\d+", str_tmp_cpp)[0])
            except ValueError:
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
    key_2_sent('g')
    get_random_wait(300, 700)
    key_2_sent('y')
    get_random_wait(500, 700)

def scan_is_end():
    found = False
    while not found:
        fd = pyautogui.locateCenterOnScreen('scan_done.png', region=SCAN_DONE_PIC, grayscale=False)
        if fd is not None:
            found = True
            break
        time.sleep(0.5)

# ======CONSTANTS========
'''
G  == target npc
Y  == talk with npc
K  == /RL MACRO

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

ADJ = 2
SCAN_DONE_PIC = (320, 614 + ADJ, 83, 36)
CLOSE_TSM = (911, 128 + ADJ)
HISTORY_BUTTON_ON_SHOP = (641, 238 + ADJ)
BUY_SEARCH = (641, 161 + ADJ)
BUY_SEARCH_BACK = (217, 178 + ADJ)
ITEM_SEARCH = (863, 220 + ADJ)
SORT_RESULT = (867, 252 + ADJ)
FIRST_ROW_POST = (446, 267 + ADJ, 36, 14)
FIRST_ROW_STACK  = (492, 267 + ADJ, 39, 14)
FIRST_ROW_BUYOUT = (815, 268 + ADJ, 89, 14)
FULL_SCAN_BUTTON = (343, 626 + ADJ)
INPUT_BOX = (377, 220 + ADJ)
BUYOUT_BUTTON = (0, 0)
AUCTION_BUTTON_ON_SHOPPING = (0, 0)
AUCTION_ON_SHOP_BIDING_PRICE_INPUT = (0, 0)
AUCTION_ON_SHOP_BUYOUT_PRICE_INPUT = (0, 0)
AUCTION_ON_SHOP_MAX_STACK_BUTTON = (0, 0)
AUCTION_ON_SHOP_POST_VOLUME_INPUT_BUTTON = (0, 0)
AUCTION_ON_SHOP_CONFIRM_BUTTON =(0, 0)


X_RATIO = 1.04
Y_RATIO = 1.04
J_RATIO = 1.85
Q_RATIO = 1.85
PORT = 'COM17'
DESKTOP = (2560, 1440)  # Related with X_RATIO, and Y_RATIO, set in arduino manually


# ======= json file structure for scan_data.json ======
'''
in file target_goods_list.json
[
    ['锚草', '阿昆达之噬', '凛冬之吻', '海潮茎杆', '流波花苞', '海妖花粉', '星光苔'],
    {                                '锚草': [0, 99999, 100, 9000, 0],
                                     '阿昆达之噬': [0, 99999, 100, 8000, 0],
                                     '凛冬之吻': [0, 99999, 100, 1200, 0],
                                     '海潮茎杆': [0, 99999, 100, 1000, 0],
                                     '流波花苞': [0, 99999, 100, 2000, 0],
                                     '海妖花粉': [0, 99999, 100, 2000, 0],
                                     '星光苔': [0, 99999, 100, 1000, 0]
    },
  
]

'''

'''
in file scan_data.json

{
'item_name':'锚草', 
'item_threshold_price': 9000, 
'item_threshold_pct': 0.70, 
'item_onshelf_lowest': 999999,
'item_onshelf_sticking_volume': 99,
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

with open('target_goods_list.json', 'r') as fp:
    target_goods_list = json.load(fp)
    all_goods_names = target_goods_list[0]               # the botting goods name list
    all_goods_to_do = target_goods_list[1]
    # [on_shelf?, threshold_on_shelf_price(lowest), sticking_volume, snip_threshold_price(highest),
    #  ship_threshold_price_percentage(first 3 rows)]

# ===== loading history and initializing data to check any new items=====
with open('scan_data.json', 'r') as fp:
    scan_data = json.load(fp)

recorded = False
for item in all_goods_names:
    for recorded_item in scan_data:
        if recorded_item.get('item_name') == item:
            recorded = True
            print(item + 'recorded')
    if not recorded:
        print(item + 'NOT recorded')
        scan_data.append({
            'item_name': item,
            'item_threshold_price': all_goods_to_do.get(item)[3],
            'item_threshold_pct': all_goods_to_do.get(item)[4],
            'item_onshelf_lowest': all_goods_to_do.get(item)[1],
            'item_onshelf_sticking_volume': all_goods_to_do.get(item)[2],
            'item_buyout_history': [],
            'item_onshelf_history': []
        })
        with open('scan_history\\' + item + '_history.json', 'w') as fp:
            json.dump([], fp, ensure_ascii=False)
with open('scan_data.json', 'w') as fp:
    json.dump(scan_data, fp, ensure_ascii=False)


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


# ===== wait to start ====
print('press F10 to start..')
while not keyboard.is_pressed('F10'):
    pass
winsound.Beep(1000, 200)
get_random_wait(1000, 1200)

# ====== start tsm ========

while True:
    open_tsm()
    action_list = [BUY_SEARCH, HISTORY_BUTTON_ON_SHOP]
    for act in action_list:
        move2(act)
        key_2_sent('l')
    logging.info('ready to start, tsm opened')
    scan_is_end()
    for goods_name in all_goods_names:
        move2(INPUT_BOX)
        get_random_wait(600, 900)
        key_2_sent('l')
        get_random_wait(600, 900)
        for i in range(10):
            key_2_sent('<')
        pyperclip.copy(goods_name)
        key_2_sent('>')
        get_random_wait(600, 900)
        key_2_sent('o')

        goods = Item()

        scan_is_end()

        move2(SORT_RESULT)
        get_random_wait(500, 600)
        key_2_sent('l')
        get_random_wait(900, 1100)
        key_2_sent('k')

        quotes = []
        for i in range(8):
            quote = goods.get(i, 0)
            if quote[2] == 0:
                quote = goods.get(i, 4)
            quotes.append(quote)
            print(quote)
        with open('scan_history\\' + goods_name + '_history.json', 'r') as fp:
            data = json.load(fp)
        data.append({   'date&time': datetime.datetime.today().strftime('%Y-%m-%d %H:%M')
                                     + ' ('+ datetime.datetime.today().strftime('%A'),
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

        # to check if the goods is the on_shelf goods:
            # check the in range 8 check the first volume bigger than the minium volume
            # check the volume is make by self?
            # check the price is lower than the lowest
            # list the goods & record

        # else to check if the 1st is lower the threshold of snipper
            # to check if the 1st is lower than % of the threshold
            # to check if the price is lower than % of the second
            # if yes ,buyout and record


