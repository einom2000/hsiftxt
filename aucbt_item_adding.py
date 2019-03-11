import json
import pandas as pd
import keyboard, sys
import shutil
import time

def value_input(display, index):
    correct = False
    while not correct:
        try:
            value = int(input(display))
            correct = True
        except ValueError:
            try:
                value = goods_to_do.get(name)[index]
                correct = True
            except TypeError:
                print('此项输入错误！')
    return value


t = time.localtime()
timestamp = time.strftime('%b-%d-%Y_%H%M', t)
BACKUP_NAME = ("target_goods_list_BACKUP_" + timestamp)
shutil.copy('target_goods_list.json', BACKUP_NAME + '.bak')
while True:
    with open('target_goods_list.json', 'r') as fp:
        data = json.load(fp)

    goods_name = data[0]
    goods_to_do = data[1]
    shows = pd.DataFrame.from_dict(goods_to_do, orient='index', columns=
                                   ['上架', '最低价', '紧盯量', '扫最高', '扫货比', '上架数', '堆数量'])
    shows.style.set_properties(**{'text-align': 'right'})
    print(shows.astype(int))
    print('please press SPACE to input! or press X to exit')

    while True:
        if keyboard.is_pressed('x'):
            sys.exit()
        elif keyboard.is_pressed(' '):
            break
        else:
            pass

    name = input('增加商品名称: ').replace(' ', '')

    is_on_shelf = value_input('是否要上架 1 / 0: ', 0)
    lowest = value_input('最低的售价: ', 1)
    stack = value_input('紧盯的数量: ', 2)
    highest = value_input('扫货最高价: ', 3)
    percent = value_input('扫货价差比: ', 4)
    on_post = value_input('上架的堆数: ', 5)
    on_stack = value_input('每堆的数量: ', 6)

    tmp = {name: [is_on_shelf, lowest, stack, highest, percent, on_post, on_stack]}
    temp_show = pd.DataFrame.from_dict(tmp, orient='index', columns=
                                       ['上架', '最低价', '紧盯量', '扫最高', '扫货比', '上架数', '堆数量'])
    temp_show. style.set_properties(**{'text-align': 'right'})

    print('增加商品名称: ' + name)
    print(temp_show.astype(int))
    print('please press Y to confirm or N to cancel! ')
    while True:
        if keyboard.is_pressed('y'):
            if name not in goods_name:
                goods_name.append(name)
            goods_to_do.update (tmp)
            data = [goods_name, goods_to_do]
            # print(goods_name)
            # print(goods_to_do)
            with open('target_goods_list.json', 'w') as fp:
                json.dump(data, fp, ensure_ascii=False)
            break
        elif keyboard.is_pressed('n'):
            print('editing canceled')
            name = ''
            tmp = {}
            break

