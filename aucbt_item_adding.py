import json
import pandas as pd
import keyboard, sys
import shutil
import time
from colorama import init, Fore, Back, Style


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

def modify(on_shelf):
    for name in data[0]:
        data[1].get(name)[0] = on_shelf
    temp_show = pd.DataFrame.from_dict(data[1], orient='index', columns=
    ['上架', '最低价', '紧盯量', '扫最高', '扫货比', '上架数', '堆数量'])
    temp_show.style.set_properties(**{'text-align': 'right'})
    print(temp_show.astype(int))
    print('please press Y to confirm or N to cancel! ')

    while True:
        if keyboard.is_pressed('y'):
            with open('target_goods_list.json', 'w') as fp:
                json.dump(data, fp, ensure_ascii=False)
            break
        elif keyboard.is_pressed('n'):
            print('editing canceled')
            break

init()
t = time.localtime()
timestamp = time.strftime('%b-%d-%Y_%H%M', t)
BACKUP_NAME = ('backup_files\\' + "target_goods_list_BACKUP_" + timestamp)
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
    print('please press SPACE to input! or press X to exit, or 9 to set all goods overlooked! or 0 to set all goods to'
          'snipper')

    while True:
        if keyboard.is_pressed('x'):
            sys.exit()
        elif keyboard.is_pressed('9'):
            modify(9)
            sys.exit()
        elif keyboard.is_pressed('0'):
            modify(0)
            sys.exit()
        elif keyboard.is_pressed(' '):
            break
        else:
            pass
    time.sleep(1)
    while True:
        name = input('增加商品名称: ').replace(' ', '')
        if name !='':
            break
    if name in goods_name:
        originals = goods_to_do.get(name).copy()
    else:
        originals = ['无数值', '无数值', '无数值', '无数值', '无数值', '无数值', '无数值']

    print(Fore.YELLOW + Style.DIM + '%s-原来上架指数是：%s' %(name, originals[0]))
    is_on_shelf = value_input(Fore.RED + Style.BRIGHT + '是否要上架 1 / 0: ', 0)
    print(Fore.YELLOW + Style.DIM + '%s-原来最低的售价是：%d' % (name, originals[1]))
    lowest = value_input(Fore.RED + Style.BRIGHT + '新的最低售价: ', 1)
    print(Fore.YELLOW + Style.DIM + '%s-原来紧盯的数量是：%d' % (name, originals[2]))
    stack = value_input(Fore.RED + Style.BRIGHT + '新的紧盯的数量: ', 2)
    print(Fore.YELLOW + Style.DIM + '%s-原来扫货最高价是：%d' % (name, originals[3]))
    highest = value_input(Fore.RED + Style.BRIGHT + '新的扫货最高价: ', 3)
    print(Fore.YELLOW + Style.DIM + '%s-原来扫货价差比是：%d' % (name, originals[4]))
    percent = value_input(Fore.RED + Style.BRIGHT + '新的扫货价差比: ', 4)
    print(Fore.YELLOW + Style.DIM + '%s-原来上架的堆数是：%d' % (name, originals[5]))
    on_post = value_input(Fore.RED + Style.BRIGHT + '新的上架的堆数: ', 5)
    print(Fore.YELLOW + Style.DIM + '%s-原来每堆的数量是：%d' % (name, originals[6]))
    on_stack = value_input(Fore.RED + Style.BRIGHT + '新的每堆的数量: ', 6)
    print(Style.RESET_ALL)

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

