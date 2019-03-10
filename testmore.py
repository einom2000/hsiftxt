

# (83, 263) KUAISUBISAI
# (315, 346) SHISHIZHANCHANG
# (400, 530) CONFIRMED
# (575, 322) jiaruzhandou
# (516, 303)(638, 338) squre jiaruzhandou
#----ABOVE ON 1280X 710

# import numpy as np
#
# a = (1, 2, 3, 4)
# b = (1,1,1,1)
# print(np.add(a, b))

# int('d')


# #
# import random, pyautogui,time,keyboard
# lst = [(357, 566),
#         (357, 609),
#         (356, 650),
#         (358, 694),]
# running = True
# t = 0
# while running:
#     ran_pos = lst[random.randint(0, 3)]
#     pyautogui.moveTo(ran_pos[0], ran_pos[1])
#     time.sleep(.5)
#     pyautogui.click()
#     time.sleep(.5)
#     t += 1
#     if keyboard.is_pressed(' ') or t >= 105:
#         running = False

import datetime
print(datetime.datetime.today().strftime('%A'))
print(datetime.datetime.today().strftime('%Y-%m-%d %H:%M') + ' ('+ datetime.datetime.today().strftime('%A') + ') :')



# #
# import json
#
#
# with open('target_goods_list.json', 'r') as fp:
#     snipper_list = json.load(fp)
# snipper_goods_names = snipper_list[0]
# snipper_goods_threshold_prc_pct = snipper_list[1]
#
# # ===== loading history and initializing data to check any new items=====
# with open('scan_data.json', 'r') as fp:
#     scan_data = json.load(fp)
#
# recorded = False
# for item in snipper_goods_names:
#     for recorded_item in scan_data:
#         if recorded_item.get('item_name') == item:
#             recorded = True
#             print(item + 'recorded')
#     if not recorded:
#         print(item + 'NOT recorded')
#         scan_data.append({
#             'item_name': item,
#             'item_threshold_price': snipper_goods_threshold_prc_pct.get(item)[0],
#             'item_threshold_pct': snipper_goods_threshold_prc_pct.get(item)[1],
#             'item_buyout_history': [],
#             'item_price_history': []
#         })
# with open('scan_data.json', 'w') as fp:
#     json.dump(scan_data, fp, ensure_ascii=False)
#
