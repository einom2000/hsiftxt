

# waiting for start 1, stop 0, none of them 99


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
    elif cur_time - last_anti_afk >= ANTI_AFT_TIME * random.randint(55, 58):
        key_2_sent(ANTI_AFT_KEY[random.randint(0, (len(ANTI_AFT_KEY)-1))])
        get_random_wait(400, 600)
        key_2_sent('s')
        last_anti_afk = time.time()
    # Cast fishing pole until found a hook is can't found th hook in 5 seconds then recast
    print('time to stop = :' + str(int(cur_time - running_elapsed ))  +  ' and time to act: '
          + str(int(cur_time - last_anti_afk)))
    if datetime.now().hour == end_time[0] and datetime.now().minute >= end_time[1]:
        running = False
        end_game()
    else:
        print('set to end at: ' + str(end_time[0]) + ':' + str(end_time[1]))
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