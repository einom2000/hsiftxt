import serial, keyboard, sys
import win32api, win32gui, winsound
import time, random, pyautogui
import logging, json
import cv2, os
from datetime import datetime
from tkinter import *

def key_2_sent(key):  # 'r' for right mouse double click, 'l' for left click, 't' for right click
    # 'o' for enter; 'u' for up; 'j' for down(jump); 'k' for macro /camp
    key_sent = str(key)
    ard.flush()
    print("Python value sent: " + key_sent)
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
    print("Python value sent: " + key_sent)
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
    print("Python value sent: " + key_sent)
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


def get_random_wait(low, high):
    # wait for a random time
    time.sleep(random.randint(low, high) / 1000)


def blur_pos_dur():
    # get a random blur relevant x and y and random time according to the constants
    x = random.randint(BLUR_PIXEL[0], BLUR_PIXEL[1]) * random.choice([-1, 1])
    y = random.randint(BLUR_PIXEL[0], BLUR_PIXEL[1]) * random.choice([-1, 1])
    t = random.randint(BLUR_DUR[0], BLUR_DUR[1])
    return x, y, t


def scope_size():
    # get searching area for the bobber
    rect = ((SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4),
            (SCREEN_WIDTH * 9 // 12, SCREEN_HEIGHT * 12 // 20))
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


def enumhandler(hwnd, lParam):
    # enumwindows' callback function
    # if mixer found, move it next to the main windows
    if win32gui.IsWindowVisible(hwnd):
        if '音量合成' in win32gui.GetWindowText(hwnd):
            win32gui.MoveWindow(hwnd, SCREEN_WIDTH, 0, 760, 500, True)


def create_mixer():
    # create mixer and allocate it after 5 seconds
    os.startfile("SndVol.exe")
    time.sleep(5)
    win32gui.EnumWindows(enumhandler, None)


def get_line(screen_shot, length):
    line = []
    for i in range(0, length):
        line.append(screen_shot.getpixel((i, 2)))
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
        while fd_hook is None:
            for img in bobber_images:
                fd_hook = pyautogui.locateCenterOnScreen(img, region=(rect[0][0], rect[0][1],
                                                                      rect[1][0], rect[1][1]),
                                                         grayscale=False, confidence=confi)
            # if searching time is too long quit loop
                if fd_hook is not None:
                    if fd_hook[1] > rect[1][1]:
                        print('too big y')
                        print(fd_hook)
                        fd_hook = None
                    else:
                        print(img)
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
                                           self.trigger_x + self.trigger_length, self.trigger_y + 1))
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
                                               self.trigger_x + self.trigger_length, self.trigger_y + 1))
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


###############################################################################################################
# Game Constant

X_RATIO = 1.04
Y_RATIO = 1.04
J_RATIO = 1.85
Q_RATIO = 1.85
PORT = 'COM17'
DESKTOP = (2560, 1440)  # Related with X_RATIO, and Y_RATIO, set in arduino manually

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
TRIGGER_LENGTH = 200
TIME_TO_RUN = 600
TIME_FOR_EACH_ROLE = 60
AFTER_GAME_END = ['v']  # hide or quit after game end
ANTI_AFT_TIME = 10
ANTI_AFT_KEY = ['z', 'x', 'c']  # 3 action shortcut key to anti AFK
CASTPOLE = 'f'  # key 'f' for cast fishing pole
ROLE_TO_LOOP = 3

# K1 = pyautogui.easeInQuad
# K2 = pyautogui.easeOutQuad
# K3 = pyautogui.easeInOutQuad
# K4 = pyautogui.easeInBounce
# K5 = pyautogui.easeInElastic

#  Game variables
infoTxt = ''
hookMissed = 0
soundMissed = 0
count = 0
running = True
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

# load standard images
bobber_images = []

logging.basicConfig(filename='running.log',
                    filemode='w',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG
                    )

ard = serial.Serial(PORT, 9600, timeout=5)
time.sleep(2)
logging.info('Serial opened and program starts!')

for i in range(1, 20 + 1):
    bobber_images.append("pp{}.png".format(i))

# looking for mixer, if not create one and move it next to the main window
while not mixer_found:
    trigger_pos = locate_mixer()
    if trigger_pos:
        mixer_found = True
    else:
        create_mixer()

# showing sound trigger bar area and the hook monitering area press STARTKEY to proceed or STOPKEY to rerun program
show_trigger = ShowBoundary(((TRIGGER_DEDENT + TRIGGER_LENGTH), 3), (trigger_pos[0], trigger_pos[1] - 1), 'orange')
show_trigger.showframe()
show_scopesize = ShowBoundary((rect[1][0] - rect[0][0], rect[1][1] - rect[0][1]), rect[0], 'cyan')
show_scopesize.showframe()

# waiting for start 1, stop 0, none of them 99
while True:
    key = check_for_key_in()
    if key == 1:
        running = True
        winsound.Beep(1000, 200)
        show_trigger.killframe()
        show_scopesize.killframe()
        del show_trigger
        del show_scopesize
        break
    elif key == 2:
        go_pause()
    elif key == 0:
        running = False
        winsound.Beep(500, 400)
        break

# game loop start
#=============================================================================================================

new_cst = CastPole(rect_center)
mouse_2_sent([620, 220])
## initialize the mouse to the pool center
print('inintialize mouse to ' + str([620, 220]))

while running:
    # First Check if the running time is longer than expected or should have anti aftk key press.
    cur_time = time.time()
    if cur_time - running_elapsed >= TIME_TO_RUN * random.randint(58, 62):
        running = False
        end_game()
    elif cur_time - last_anti_afk >= ANTI_AFT_TIME * random.randint(58, 62):
        key_2_sent(ANTI_AFT_KEY[random.randint(0, (len(ANTI_AFT_KEY)-1))])
        get_random_wait(400, 600)
        key_2_sent('s')
        last_anti_afk = time.time()
    # Cast fishing pole until found a hook is can't found th hook in 5 seconds then recast
    print('time to stop = :' + str(int(cur_time - running_elapsed ))  +  ' and time to act: '
          + str(int(cur_time - last_anti_afk)))
    while hook_found is None:
        get_random_wait(500, 700)
        new_cst.cast()
        # Looking for the hook
        hook_found = new_cst.find_hooker(rect, 0.9)
    # move mouse to the blurred postion of the found hook

    x, y, t = blur_pos_dur()
    get_random_wait(500, 600)
    curr_mouse = pyautogui.position()
    rlt_x = int(hook_found[0] - curr_mouse[0])
    rlt_y = int(hook_found[1] - curr_mouse[1])
    while abs(rlt_x) > 20 or abs(rlt_y) > 20:
        if abs(rlt_x) > 175 :
            rlt_x = 175 * (rlt_x / abs(rlt_x))
        if abs(rlt_y) > 175 :
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

    print('fish couter: ' + str(fish_counter))
    print('hook_missing: ' + str(hook_missing_counter))
    print('sound_missing: ' + str(sound_missing_counter))
