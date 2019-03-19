import pyautogui
import keyboard
import time

while True:
    while not keyboard.is_pressed(','):
        pass
    print(pyautogui.position())
    time.sleep(3)
