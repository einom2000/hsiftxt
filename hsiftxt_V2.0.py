# Auto Simple Fishing v2.0
# No overlay windows
# No info. windows during fishing
# will have a text windows after fishing
# auto close wow
# auto anti-AFK
# optimized sound detect

import pyautogui, win32gui, keyboard
import time, random, winsound,os
from tkinter import *

# user options as constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
BLUR_PIXEL = [6, 16]
BLUR_DUR = [250, 400]
SOUND_THRESHOLD = 0.45
HAND_SHAKE_FACTOR = 0
START_KEY = 'F10'
STOP_KEY = 'F12'
TIME_TO_RUN = 480
ANTI_AFT_TIME = 10


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
        height = mixer_rect[3] -mixer_rect[1]
        x = mixer_rect[0] + int(width * 0.13)
        y = mixer_rect[1] + int(height * (1 - SOUND_THRESHOLD * 0.85))
        mixer_trigger = (x, y)
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


def get_line(screenshot, length):
    line = []
    for i in range(0, length):
        line.append(screenshot.getpixel((i, 2)))
    return line


class CastPole:
    # cast the pole and looking for the dobber
    # move mouse to the dobber

    def __init__(self, mouse_position):
        self.mouse_pos = mouse_position

    def cast(self):
        # get a blur
        blur_x, blur_y, dur_t = blur_pos_dur()
        pyautogui.moveTo(self.mouse_pos[0], self.mouse_pos[1], 0.3, pyautogui.easeInQuad)
        self.mouse_pos = tuple(map(lambda x, y: x + y, self.mouse_pos,
                                      (blur_x * 3, blur_y * 3)))
        # right double click
        pyautogui.rightClick(self.mouse_pos[0], self.mouse_pos[1], dur_t)
        get_random_wait(100, 300)
        pyautogui.rightClick(self.mouse_pos[0], self.mouse_pos[1], dur_t)
        get_random_wait(500, 800)

    def find_hooker(self, rect, confi=None):
        if not confi: confi = 0.5
        found_hook = False
        t = time.time()
        while not found_hook:
            for img in dobber_images:
                found_hook = pyautogui.locateCenterOnScreen(img, region=(rect[0][0], rect[0][1],
                                                                        rect[1][0], rect[1][0]),
                                                            grayscale=True, confidence=confi)
                if found_hook:
                    break
            # if searching time is too long quit loop
            if time.time() - t >= 5.0:
                break
        return found_hook


class Listen2mixer:
    def __init__(self, trigger):
        self.trigger_x = trigger[0] - 8
        self.trigger_y = trigger[1]
        self.trigger_length = 20
        img = pyautogui.screenshot(region=(self.trigger_x, self.trigger_y - 1,
                                           self.trigger_x + self.trigger_length, self.trigger_y + 1))
        self.silent = get_line(img, self.trigger_length)
        print(self.silent)
        print(self.trigger_x, self.trigger_y - 1, self.trigger_x + self.trigger_length, self.trigger_y + 1)

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

# Game variables
infoTxt = ''
hookMissed = 0
soundMissed = 0
count = 0
running = True
mixer_found = False
trigger_pos = ()

# load standard images
dobber_images = []
for i in range(1, 10+1):
    dobber_images.append("pp{}.png".format(i))


# looking for mixer and get the trigger pixel in tirgger_pos
while not mixer_found:
    trigger_pos = locate_mixer()
    if trigger_pos:
        # pyautogui.moveTo(trigger_pos[0], trigger_pos[1], 0.2)
        mixer_found = True
    else:
        create_mixer()

print(trigger_pos)
lstn = Listen2mixer(trigger_pos)
if lstn.listen():
    print('yes!')
else:
    print('no!')

sys.exit()

# sudo
# rect = scope_size()
# cst = CastPole((300, 800))
# cst.cast()
# fd = cst.find_hooker(rect, 0.6)
# if fd:
#     pyautogui.moveTo(fd[0], fd[1], 0.5)
#     print(fd)
