# Auto Simple Fishing v2.0
# No overlay windows
# No info. windows during fishing
# will have a text windows after fishing
# auto close wow
# auto anti-AFK
# optimized sound detect

import pyautogui, win32gui, keyboard
import time, random, winsound
from tkinter import *

# user options as constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
BLUR_PIXEL = [6, 16]
BLUR_DUR = [250, 400]
SOUND_THRESHOLD = 0.50
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
        print(x, y)
        mixer_trigger = (x, y)
    else: mixer_trigger = None
    return mixer_trigger

# Game variables
infoTxt = ''
hookMissed = 0
soundMissed = 0
count = 0
running = True

# load standard images
dobber_images = []
for i in range(1, 10+1):
    dobber_images.append("pp{}.png".format(i))


class CastPole:
    # cast the pole and looking for the dobber
    # move mouse to the dobber

    def __init__(self, mouse_position):
        self.mouse_pos = mouse_position

    def cast(self):
        # get a blur
        blur_x, blur_y, dur_t = blur_pos_dur()
        pyautogui.moveTo(self.mouse_pos[0], self.mouse_pos[1], 0.3, pyautogui.easeInQuad)
        self.mouse_pos =tuple(map(lambda x, y: x + y, self.mouse_pos,
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
        print(rect)
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

class Listen2mixer():
    def __init(self, trigger):
        self.strigger = trigger

    def listen(self):
        t = time.time()

tmp = locate_mixer()
if tmp:
    pyautogui.moveTo(tmp[0], tmp[1], 0.2)

# sudo
# rect = scope_size()
# cst = CastPole((300, 800))
# cst.cast()
# fd = cst.find_hooker(rect, 0.6)
# if fd:
#     pyautogui.moveTo(fd[0], fd[1], 0.5)
#     print(fd)
