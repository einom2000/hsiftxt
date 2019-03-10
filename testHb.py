import keyboard, pyautogui,time

while True:
    while keyboard.is_pressed(' '):
        print(pyautogui.position())
        time. sleep(1)