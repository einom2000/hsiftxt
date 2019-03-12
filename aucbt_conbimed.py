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
    # ']' for ctrl-a, '[' for ctrl-c
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
    img = Image.open('ocr_files\\' + image)
    img = PIL.ImageOps.invert(img)
    img.save('ocr_files\\' + '_con_' + image)
    img = cv2.imread('ocr_files\\' + '_con_' + image)
    img = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 3, 21)
    cv2.imwrite('ocr_files\\' + '_dnos_' + image, img)
    return img



class Item():
    def __init__(self):
        self.item_post = FIRST_ROW_POST
        self.item_stack = FIRST_ROW_STACK
        self.item_buyout = FIRST_ROW_BUYOUT

    def get(self, item_row , adjust):
        ####   post   ####
        pyautogui.screenshot('ocr_files\\' + str(item_row)+'_row_post.jpg',
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
            post_num = 1
        except IndexError:
            post_num = 1
        ####   stack   ####
        pyautogui.screenshot('ocr_files\\' + str(item_row)+'_row_stack.jpg',
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
        except IndexError:
            stack_num = 0
        ####   buyout   ####
        pyautogui.screenshot('ocr_files\\' + str(item_row)+'_row_buyout.jpg',
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

def scan_is_end():
    found = False
    while not found:
        fd = pyautogui.locateCenterOnScreen('scan_done.png', region=SCAN_DONE_PIC, grayscale=False)
        if fd is not None:
            found = True
            break
        time.sleep(0.5)

def input_box(positon, scr):
    move2(positon)
    get_random_wait(100, 200)
    key_2_sent('l')
    get_random_wait(100, 200)
    key_2_sent(']')
    get_random_wait(100, 200)
    pyperclip.copy(scr)
    key_2_sent('>')
    get_random_wait(100, 200)
    key_2_sent('o')
    get_random_wait(100, 200)


# ================================fish=====================================
def create_mixer():
    # create mixer and allocate it after 5 seconds
    os.startfile("SndVol.exe")
    time.sleep(5)
    win32gui.EnumWindows(enumhandler, None)

def go_pause():
    while not keyboard.is_pressed(PAUSE_KEY):
        if keyboard.is_pressed(STOP_KEY):
            end_game()
        pass


def end_game():
    winsound.Beep(1000, 300)
    time.sleep(0.300)
    winsound.Beep(1000, 300)
    for short_cut_key in AFTER_GAME_END:
        key_2_sent(short_cut_key)
        get_random_wait(400, 600)
    sys.exit()
    pass


def blur_pos_dur():
    # get a random blur relevant x and y and random time according to the constants
    x = random.randint(BLUR_PIXEL[0], BLUR_PIXEL[1]) * random.choice([-1, 1])
    y = random.randint(BLUR_PIXEL[0], BLUR_PIXEL[1]) * random.choice([-1, 1])
    t = random.randint(BLUR_DUR[0], BLUR_DUR[1])
    return x, y, t


def scope_size():
    # get searching area for the bobber
    rect = ((SCREEN_WIDTH * 10 // 36, SCREEN_HEIGHT // 4),
            (SCREEN_WIDTH * 9 // 12, SCREEN_HEIGHT * 15 // 20))
    return rect


def locate_mixer():
    # locate a trigger pixel in a mixer via proportion
    # if there is a mixer next to the main window
    # pyautogui.moveTo(SCREEN_WIDTH + 250, SCREEN_HEIGHT // 4)
    # pyautogui.click()
    mouse_2_sent([SCREEN_WIDTH + 250, SCREEN_HEIGHT // 4])
    key_2_sent('l')
    mixer_txt = win32gui.GetWindowText(win32gui.GetForegroundWindow())
    mixer_txt = mixer_txt[:4]
    if mixer_txt == "音量合成":
        mixer_rect = win32gui.GetWindowRect(win32gui.GetForegroundWindow())
        width = mixer_rect[2] - mixer_rect[0]
        height = mixer_rect[3] - mixer_rect[1]
        mixer_x = mixer_rect[0] + int(width * 0.13)
        mixer_y = mixer_rect[1] + int(height * (1 - SOUND_THRESHOLD * 0.85))
        mixer_trigger = (mixer_x, mixer_y)
    else:
        mixer_trigger = None
    return mixer_trigger


def get_line(screen_shot, length):
    line = []
    for i in range(0, length):
        line.append(screen_shot.getpixel((i, 1)))
    return line


def get_fish():
    # ensure a right click to have a fish after bit
    key_2_sent('t')
    get_random_wait(800, 1300)


def check_for_key_in():
    if keyboard.is_pressed(START_KEY):
        key = 1
    elif keyboard.is_pressed(STOP_KEY):
        key = 0
    elif keyboard.is_pressed(PAUSE_KEY):
        key = 2
    else:
        key = 99
    return key


class CastPole:
    # cast the pole and looking for the bobber
    # move mouse to the bobber
    def __init__(self, mouse_position):
        self.mouse_pos = mouse_position

    def cast(self):
        # get a blur
        blur_x, blur_y, dur_t = blur_pos_dur()
        self.mouse_pos = pyautogui.position()
        self.mouse_pos = tuple(map(lambda x, y: x + y, self.mouse_pos,
                                   (blur_x * 15, blur_y * 15)))
        # cast command
        key_2_sent('f')
        get_random_wait(600, 900)
        winsound.Beep(1000, 300)

    def find_hooker(self, rect, confi=None):
        global hook_missing_counter
        if not confi: confi = 0.5
        fd_hook = None
        tm = time.time()
        # print((rect[0][0], rect[0][1],rect[1][0], rect[1][1]))
        while fd_hook is None:
            for img in bobber_images:
                fd_hook = pyautogui.locateCenterOnScreen(img, region=(rect[0][0], rect[0][1],
                                                                      rect[1][0] - rect[0][0], rect[1][1] - rect[0][1]),
                                                         grayscale=False, confidence=confi)
            # if searching time is too long quit loop
                if fd_hook is not None:
                    # if fd_hook[1] > rect[1][1]:
                    if fd_hook[1] > rect[1][1] or \
                       fd_hook[1] < rect[0][1] or \
                       fd_hook[0] > rect[1][0] or \
                       fd_hook[0] < rect[0][0]:
                        pass
                        print('too far away!')
                        print(fd_hook)
                        fd_hook = None
                    else:
                        good_bobber[bobber_images.index(img)] += 1
                        print(good_bobber)
                        break

            if time.time() - tm >= 5.0:
                hook_missing_counter += 1
                break
        return fd_hook


class Listen2mixer:
    def __init__(self, trigger):
        self.trigger_x = trigger[0] - TRIGGER_DEDENT
        # 8 can be adjusted
        self.trigger_y = trigger[1]
        self.trigger_length = TRIGGER_LENGTH
        img = pyautogui.screenshot(region=(self.trigger_x, self.trigger_y - 1,
                                           self.trigger_length, 2))
        self.silent = get_line(img, self.trigger_length)

    def listen(self):
        global sound_missing_counter
        t = time.time()
        listening = True
        bingo = False
        pause = False
        stop = False
        while listening:
            if keyboard.is_pressed(STOP_KEY):
                stop = True
                break
            elif keyboard.is_pressed(PAUSE_KEY):
                pause = True
                break
            new = pyautogui.screenshot(region=(self.trigger_x, self.trigger_y - 1,
                                               self.trigger_length, 2))
            new_line = get_line(new, self.trigger_length)
            if new_line != self.silent:
                bingo = True
                listening = False
            elif time.time() - t >= 17.0:
                listening = False
                bingo = False
        return bingo, pause, stop


class ShowBoundary:
    def __init__(self, rec_size, top_left, color):
        self.trigger_boards = list()
        self.color = color
        rec_top = str(rec_size[0] + 6) + "x3+" + str(top_left[0] - 3) + "+" + str(top_left[1] - 3)
        rec_bottom = str(rec_size[0] + 6) + "x3+" + str(top_left[0] - 3) + "+" + str(top_left[1] + rec_size[1])
        rec_left = str("3x" + str(rec_size[1] + 3 - 1) + "+" + str(top_left[0] - 3) + "+"
                       + str(top_left[1] - 3))
        rec_right = str("3x" + str(rec_size[1] + 3 - 1) + "+" + str(top_left[0] + rec_size[0]) + "+"
                        + str(top_left[1] - 3))
        geo = (rec_top, rec_bottom, rec_left, rec_right)

        for i in range(0, 3 + 1):
            self.trigger_boards.append(Tk())
        for i in range(0, 3 + 1):
            self.trigger_boards[i].overrideredirect(1)
            self.trigger_boards[i].attributes("-topmost", True)
            self.trigger_boards[i].config(bg=self.color)
            self.trigger_boards[i].geometry(geo[i])

    def showframe(self):
        for i in range(0, 3 + 1):
            self.trigger_boards[i].update()
        pass

    def killframe(self):
        for i in range(0, 3 + 1):
            self.trigger_boards[i].destroy()
# ===============================fish_end====================================
# ======CONSTANTS========
'''
G  == target npc
Y  == talk with npc
H  == /RL MACRO
- == /LOGOUT /MACRO

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

ADJ = -2
SCAN_DONE_PIC = (320, 614 + ADJ, 83, 36)
CLOSE_TSM = (911, 128 + ADJ)
CLOSE_TSM_ICON =(897, 112, 40, 40)
RELOAD_SUCCESS =(1036, 709, 180, 50)
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
BUYOUT_BUTTON_ON_SHOP = (799, 626 + ADJ)
AUCTION_BUTTON_ON_SHOP = (565, 626 + ADJ)
AUCTION_ON_SHOP_BIDING_PRICE_INPUT = (687, 431 + ADJ)
AUCTION_ON_SHOP_BUYOUT_PRICE_INPUT = (686, 453 + ADJ)
AUCTION_12_TIME = (590, 395 + ADJ)
AUCTION_ON_SHOP_STACK_INPUT = (683, 350 + ADJ)
AUCTION_ON_SHOP_POST_INPUT = (597, 350 + ADJ)
AUCTION_ON_SHOP_CONFIRM_BUTTON = (593, 500 + ADJ)
ANTI_AFK = 480
SCAN_ROW = 5
SELLER = (567, 60)  # x and length
SCAN_PERIOD = (120, 240)
END_TIME = [random.randint(3, 4), random.randint(10, 30)]

X_RATIO = 1.04
Y_RATIO = 1.04
J_RATIO = 1.85
Q_RATIO = 1.85
PORT = 'COM17'
DESKTOP = (2560, 1440)  # Related with X_RATIO, and Y_RATIO, set in arduino manually

# ================================fishs=========================================
# ===============================fish_end=======================================
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
BLUR_PIXEL = [1, 3]
BLUR_DUR = [250, 400]
SOUND_THRESHOLD = 0.40
HAND_SHAKE_FACTOR = 0
START_KEY = 'F10'
STOP_KEY = 'F12'
PAUSE_KEY = 'F11'
TRIGGER_DEDENT = 8
TRIGGER_LENGTH = 400
TIME_TO_RUN = 10
TIME_FOR_EACH_ROLE = 60
AFTER_GAME_END = ['v']  # hide or quit after game end
ANTI_AFT_TIME = 8
ANTI_AFT_KEY = ['z', 'x', 'c']  # 3 action shortcut key to anti AFK
CASTPOLE = 'f'  # key 'f' for cast fishing pole

infoTxt = ''
hookMissed = 0
soundMissed = 0
count = 0
pause_is_pressed = False
stop_is_pressed = False
mixer_found = False
hook_found = None
trigger_pos = ()
running_elapsed = time.time()
last_anti_afk = time.time()
rect = scope_size()
rect_center = (int((rect[1][0] - rect[0][0]) / 2 + rect[0][0]),
               int((rect[1][1] - rect[0][1]) / 2 + rect[0][1]))
fish_counter = 0
hook_missing_counter = 0
sound_missing_counter = 0
end_time = [random.randint(6, 7), random.randint(10, 30)]

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


# ===============================fish_end=======================================


with open('target_goods_list.json', 'r') as fp:
    target_goods_list = json.load(fp)
    all_goods_names = target_goods_list[0]               # the botting goods name list
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

# ================================fishs=========================================
bobber_images = []
good_bobber = []

time.sleep(2)

for i in range(1, 20 + 1):
    bobber_images.append("pp{}.png".format(i))
    good_bobber.append(0)

while not mixer_found:
    trigger_pos = locate_mixer()
    if trigger_pos:
        mixer_found = True
    else:
        create_mixer()

show_trigger = ShowBoundary(((TRIGGER_DEDENT + TRIGGER_LENGTH), 3), (trigger_pos[0], trigger_pos[1] - 1), 'orange')
show_trigger.showframe()
show_scopesize = ShowBoundary((rect[1][0] - rect[0][0], rect[1][1] - rect[0][1]), rect[0], 'cyan')
show_scopesize.showframe()


# ===============================fish_end=======================================


# ===== wait to start ====
print('press F10 to start..')
while not keyboard.is_pressed('F10'):
    pass
winsound.Beep(1000, 200)
show_trigger.killframe()
show_scopesize.killframe()
del show_trigger
del show_scopesize
new_cst = CastPole(rect_center)
# ====== start tsm ========
t = time.time()
open_tsm()
action_list = [BUY_SEARCH, HISTORY_BUTTON_ON_SHOP]
for act in action_list:
    move2(act)
    key_2_sent('l')
logging.info('ready to start, tsm opened')

while True:

    # timetable for fishing during a day
    if 18 > datetime.datetime.now().hour >= 15:
        TIME_TO_RUN = random.randint(9, 12)
    elif datetime.datetime.now().hour >= 18:
        TIME_TO_RUN = random.randint(5, 6)
    else:
        TIME_TO_RUN = random.randint(15, 20)
    # force to end
    if datetime.datetime.now().hour == END_TIME[0] and datetime.datetime.now().minute >= END_TIME[1]:
        sys.exit()
    # anti AFK
    if time.time() - t >= ANTI_AFK:
        key_2_sent('k')
        get_random_wait(1000, 2000)
        key_2_sent('h')
        while pyautogui.locateCenterOnScreen('reload_success.png', region=RELOAD_SUCCESS) is None:
            pass
        t = time.time()
        open_tsm()
        action_list = [BUY_SEARCH, HISTORY_BUTTON_ON_SHOP]
        for act in action_list:
            move2(act)
            key_2_sent('l')
        logging.info('wow reloaded, tsm opened')

    scan_is_end()
    for goods_name in all_goods_names:

        input_box(INPUT_BOX, goods_name)

        goods = Item()

        scan_is_end()

        quotes = []
        for i in range(SCAN_ROW):
            quote = goods.get(i, 0)
            # if quote[2] == 0:
            #     quote = goods.get(i, 4)
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
        # goods name = 'ABC'
        # goods_to_do ={"暗月火酒": [1, 13000, 5, 9000, 7, 1, 1]}
        # quotes

        # to check if the goods is the on_shelf goods:
        on_shelf = all_goods_to_do.get(goods_name)[0]
        if on_shelf == 1:
            on_shelf_lowest = all_goods_to_do.get(goods_name)[1]
            on_shelf_sticking_volume = all_goods_to_do.get(goods_name)[2]
            on_shelf_post = random.randint(1, all_goods_to_do.get(goods_name)[5])
            on_shelf_stack = all_goods_to_do.get(goods_name)[6]
            quit_on_shelf =0
            for i in range(SCAN_ROW):
                try:
                    if quotes[i][1] >= on_shelf_sticking_volume:
                        fd = pyautogui.locateCenterOnScreen('self.png', region=
                            (SELLER[0]-10, FIRST_ROW_POST[1] + i * 19 - 5, SELLER[1] + 10, FIRST_ROW_POST[3] + 5))
                        fd2 = pyautogui.locateCenterOnScreen('self2.png', region=
                            (SELLER[0]-10, FIRST_ROW_POST[1] + i * 19 - 5, SELLER[1] + 10, FIRST_ROW_POST[3] + 5))
                        print(fd, fd2)
                        if fd is None and fd2 is None and quotes[i][2] >= on_shelf_lowest * 100:
                            print((SELLER[0], FIRST_ROW_POST[1] + i * 19 + 5))
                            move2((SELLER[0], FIRST_ROW_POST[1] + i * 19 + 5))
                            key_2_sent('l')
                            move2(AUCTION_BUTTON_ON_SHOP)
                            key_2_sent('l')
                            input_box(AUCTION_ON_SHOP_STACK_INPUT, on_shelf_stack)
                            input_box(AUCTION_ON_SHOP_POST_INPUT, on_shelf_post)
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
                                                                     + ' ('+ datetime.datetime.today().strftime('%A'),
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
        if on_shelf == 0:
            threshold_price = all_goods_to_do.get(goods_name)[3] * 100
            print('threshold_price = ' + str(threshold_price))
            triger_pct = all_goods_to_do.get(goods_name)[4] / 100
            print(triger_pct)
            if triger_pct > 1:
                triger_pct = 0.7
            if quotes[0][2] != 0 and quotes[1][2] !=0 and quotes[0][2] / quotes[1][2] <= triger_pct \
                and quotes[0][2] <= threshold_price:
                move2((FIRST_ROW_POST[0], FIRST_ROW_POST[1] + 9))
                get_random_wait(100, 300)
                key_2_sent('l')
                get_random_wait(100, 300)
                move2(BUYOUT_BUTTON_ON_SHOP)
                key_2_sent('l')
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
    get_random_wait(1000, 2000)
    LOGOUT_WOW_ICON = (49, 93, 40, 40)
    key_2_sent('-')
    while pyautogui.locateCenterOnScreen('wow_icon.png', region=LOGOUT_WOW_ICON) is None:
        pass
    get_random_wait(1200, 1500)
    key_2_sent('u')
    get_random_wait(500, 700)
    key_2_sent('u')
    get_random_wait(500, 700)
    key_2_sent('o')
    while pyautogui.locateCenterOnScreen('reload_success.png', region=RELOAD_SUCCESS) is None:
        pass
    mouse_2_sent([620, 220])
    # ==================================fishting starts===================================================
    running = True
    cur_time = time.time()
    fishing_time = TIME_TO_RUN * random.randint(58, 62)
    while running:

        while hook_found is None:
            get_random_wait(500, 700)
            new_cst.cast()
            # Looking for the hook
            hook_found = new_cst.find_hooker(rect, 0.88)
        # move mouse to the blurred postion of the found hook

        x, y, t = blur_pos_dur()
        get_random_wait(500, 600)
        curr_mouse = pyautogui.position()
        rlt_x = int(hook_found[0] - curr_mouse[0])
        rlt_y = int(hook_found[1] - curr_mouse[1])
        while abs(rlt_x) > 8 or abs(rlt_y) > 8:
            if abs(rlt_x) > 175:
                rlt_x = 175 * (rlt_x / abs(rlt_x))
            if abs(rlt_y) > 175:
                rlt_y = 175 * (rlt_y / abs(rlt_y))
            mouse_2_rtv([rlt_x + x, rlt_y + y])
            print('relative move: ' + str([rlt_x + x, rlt_y + y]))
            curr_mouse = pyautogui.position()
            rlt_x = int(hook_found[0] - curr_mouse[0])
            rlt_y = int(hook_found[1] - curr_mouse[1])

        get_random_wait(300, 500)

        listening = Listen2mixer(trigger_pos)
        listen_result, pause_is_pressed, stop_is_pressed = listening.listen()
        if pause_is_pressed:
            listen_result = False
            stop_is_pressed = False
            go_pause()
        if stop_is_pressed:
            listen_result = False
            running = False
            end_game()
        if listening.listen():
            get_fish()
            fish_counter += 1
            hook_found = None
            winsound.Beep(500, 300)
            get_random_wait(400, 700)
        else:
            sound_missing_counter += 1
            hook_found = None
            winsound.Beep(1200, 300)
            get_random_wait(600, 900)

        # check if stop key or pause key has been pressed
        check_key = check_for_key_in()
        if check_key == 0:
            running = False
        elif check_key == 2:
            go_pause()
        t2 = time.time() - cur_time
        if t2 >= fishing_time:
            running = False

        print('fish couter: ' + str(fish_counter))
        print('hook_missing: ' + str(hook_missing_counter))
        print('sound_missing: ' + str(sound_missing_counter))
        print('there are ' + str(int(fishing_time - t2)) + ' seconds to fish.')

    get_random_wait(1000, 2000)
    LOGOUT_WOW_ICON = (49, 93, 40, 40)
    key_2_sent('-')
    while pyautogui.locateCenterOnScreen('wow_icon.png', region=LOGOUT_WOW_ICON) is None:
        pass
    get_random_wait(1200, 1500)
    key_2_sent('j')
    get_random_wait(500, 700)
    key_2_sent('j')
    get_random_wait(500, 700)
    key_2_sent('o')
    while pyautogui.locateCenterOnScreen('reload_success.png', region=RELOAD_SUCCESS) is None:
        pass

    if datetime.datetime.now().hour == END_TIME[0] and datetime.datetime.now().minute >= END_TIME[1]:
        sys.exit()

