import keyboard, pyautogui,time
while True:
    if keyboard.is_pressed(' '):
        print(pyautogui.position())
        time.sleep(1)



