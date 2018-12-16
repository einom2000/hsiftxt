# Auto Simple Fishing v2.0
# No overlay windows
# No info. windows during fishing
# will have a text windows after fishing
# auto close wow
# auto anti-AFK
# optimized sound detect

import pyautogui, win32gui, keyboard
import time, random, winsound, os, sys
from tkinter import *

# user options as constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
BLUR_PIXEL = [1, 6]
BLUR_DUR = [250, 400]
SOUND_THRESHOLD = 0.40
HAND_SHAKE_FACTOR = 0
START_KEY = 'F10'
STOP_KEY = 'F12'
TIME_TO_RUN = 480
AFTER_GAME_END = ['v']
ANTI_AFT_TIME = 10
ANTI_AFT_KEY = ['f4', 'space']

K1 = pyautogui.easeInQuad
K2 = pyautogui.easeOutQuad
K3 = pyautogui.easeInOutQuad
K4 = pyautogui.easeInBounce
K5 = pyautogui.easeInElastic

def check_for_stop():
    key_in = check_for_key_in()
    if key_in == 0: return False
    else: return True


def end_game():
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
    # get searching area for the dobber
    rect = ((SCREEN_WIDTH // 6, SCREEN_HEIGHT // 9),
            (SCREEN_WIDTH * 5 // 6, SCREEN_HEIGHT * 9 // 10))
    return rect


def locate_mixer():
    # locate a trigger pixel in a mixer via proportion
    # if there is a mixer next to the main window
    pyautogui.moveTo(SCREEN_WIDTH + 250, SCREEN_HEIGHT // 4)
    pyautogui.click()
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


def enumHandler(hwnd, lParam):
    # enumwindows' callback function
    # if mixer found, move it next to the main windows
    if win32gui.IsWindowVisible(hwnd):
        if '音量合成' in win32gui.GetWindowText(hwnd):
            win32gui.MoveWindow(hwnd, SCREEN_WIDTH, 0, 760, 500, True)


def create_mixer():
    # create mixer and allocate it after 5 seconds
    os.startfile("SndVol.exe")
    time.sleep(5)
    win32gui.EnumWindows(enumHandler, None)


def get_line(screen_shot, length):
    line = []
    for i in range(0, length):
        line.append(screen_shot.getpixel((i, 2)))
    return line

def get_fish():
    # ensure a rightclick to have a fish after bit
    pyautogui.rightClick()
    get_random_wait(200, 300)
    pyautogui.rightClick()


def check_for_key_in():
    if keyboard.is_pressed(START_KEY):
        key = 1
    elif keyboard.is_pressed(STOP_KEY):
        key = 0
    else:
        key = 99
    return key


class CastPole:
    # cast the pole and looking for the dobber
    # move mouse to the dobber

    def __init__(self, mouse_position):
        self.mouse_pos = mouse_position

    def cast(self):
        # get a blur
        blur_x, blur_y, dur_t = blur_pos_dur()
        pyautogui.moveTo(self.mouse_pos[0], self.mouse_pos[1], 0.3, random.choice([K1, K2, K3, K4, K5]))
        self.mouse_pos = tuple(map(lambda x, y: x + y, self.mouse_pos,
                                      (blur_x * 3, blur_y * 3)))
        # right double click
        pyautogui.rightClick(self.mouse_pos[0], self.mouse_pos[1], dur_t)
        get_random_wait(100, 300)
        pyautogui.rightClick(self.mouse_pos[0], self.mouse_pos[1], dur_t)
        get_random_wait(500, 800)

    def find_hooker(self, rect, confi=None):
        if not confi: confi = 0.5
        fd_hook = None
        tm = time.time()
        while fd_hook is None:
            for img in dobber_images:
                fd_hook = pyautogui.locateCenterOnScreen(img, region=(rect[0][0], rect[0][1],
                                                                      rect[1][0], rect[1][1]),
                                                         grayscale=True, confidence=confi)
                # print((rect[0][0], rect[0][1], rect[1][0], rect[1][1]))
                # print(img)
                # print(fd_hook)
            # if searching time is too long quit loop
            if time.time() - tm >= 5.0:
                # print('time is up', fd_hook, '=!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                break
        return fd_hook


class Listen2mixer:
    def __init__(self, trigger):
        self.trigger_x = trigger[0] - 8
        self.trigger_y = trigger[1]
        self.trigger_length = 150
        img = pyautogui.screenshot(region=(self.trigger_x, self.trigger_y - 1,
                                           self.trigger_x + self.trigger_length, self.trigger_y + 1))
        self.silent = get_line(img, self.trigger_length)
        # print(self.silent)
        # print(self.trigger_x, self.trigger_y - 1, self.trigger_x + self.trigger_length, self.trigger_y + 1)
        # pyautogui.moveTo(self.trigger_x + self.trigger_length, self.trigger_y + 1)

    def listen(self):
        t = time.time()
        listening = True
        bingo = False
        while listening:
            new = pyautogui.screenshot(region=(self.trigger_x, self.trigger_y - 1,
                                               self.trigger_x + self.trigger_length, self.trigger_y + 1))
            new_line = get_line(new, self.trigger_length)
            if new_line != self.silent:
                print(self.silent)
                print(new_line)
                bingo = True
                listening = False
            elif time.time() - t >= 17.0:
                listening = False
        return bingo


###############################################################################################################
# Game variables
infoTxt = ''
hookMissed = 0
soundMissed = 0
count = 0
running = True
mixer_found = False
hook_found = None
trigger_pos = ()
running_elapsed = time.time()
last_anti_afk = time.time()
rect = scope_size()
rect_center = (int((rect[1][0] - rect[0][0]) / 2 + rect[0][0]),
               int((rect[1][1] - rect[0][1]) / 2 + rect[0][1]))

# load standard images
dobber_images = []
for i in range(1, 10+1):
    dobber_images.append("pp{}.png".format(i))

# waiting for start 1, stop 0, none of them 99
while True:
    key = check_for_key_in()
    if key == 1:
        running = True
        winsound.Beep(1000, 200)
        break
    elif key == 0:
        running = False
        winsound.Beep(500, 400)
        break

# game loop start
#=============================================================================================================
while running:
    # First Check if the running time is longer than expected or should have anti aftk key press.
    cur_time = time.time()
    if cur_time - running_elapsed >= TIME_TO_RUN * 3600:
        running = False
        end_game()
    elif cur_time - last_anti_afk >= ANTI_AFT_TIME * 60:
        for i in range(0, len(ANTI_AFT_KEY)):
            pyautogui.press(ANTI_AFT_KEY[i])
            get_random_wait(400, 600)
        last_anti_afk = time.time()

    # looking for mixer, if not create one and move it next to the main window
    while not mixer_found:
        trigger_pos = locate_mixer()
        if trigger_pos:
            mixer_found = True
        else:
            create_mixer()

    while running:
        # checking for time lapsed and STOP_KEY to quit
        if time.time() - running_elapsed >= TIME_TO_RUN or check_for_key_in() == 99:
            running = False
        # Cast fishing pole until found a hook is can't found th hook in 5 seconds then recast
        new_cst = CastPole(rect_center)
        while hook_found is None:
            new_cst.cast()
            # Looking for the hook
            hook_found = new_cst.find_hooker(rect, 0.5)
        # move mouse to the blurred postion of the found hook
        # print("found hook!" + str(hook_found))
        x, y, t = blur_pos_dur()
        pyautogui.moveTo(hook_found[0] + x, hook_found[1] + y, t * 2 / 1000, random.choice([K1, K2, K3, K4, K5]))
        # # checking the mixer for 15 seconds
        listening = Listen2mixer(trigger_pos)
        if listening.listen():
            # print('yes!')
            get_fish()
        else:
            pass
            # print('no!')

    # check if stop key has been pressed
    running = check_for_stop()


