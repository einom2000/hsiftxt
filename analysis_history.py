import keyboard, pyautogui,time
import json
import matplotlib.pyplot as plt
import pandas as pd
import glob, numpy
import os
plt.rcParams.update({'figure.max_open_warning': 0})


def history_clean(goods_file_name):
    with open(goods_file_name, 'r') as fp:
        data = json.load(fp)
    new_data = []
    for item in data:
        if 0 in item.values():
            cancel = True
        elif (item.get('1st_quote_buyout') / (item.get('2nd_quote_buyout') + 0.01)) > 3 \
              or (item.get('1st_quote_buyout') / (item.get('2nd_quote_buyout') + 0.01)) < 0.3 \
              or (item.get('3rd_quote_buyout') / (item.get('2nd_quote_buyout') + 0.01)) > 3 \
              or (item.get('3rd_quote_buyout') / (item.get('2nd_quote_buyout') + 0.01)) < 0.3:
            cancel = True
        elif item.get('1st_quote_post') > 200 or item.get('1st_quote_stack') > 200 \
            or item.get('2nd_quote_post') > 200 or item.get('2nd_quote_stack') > 200 \
            or item.get('3rd_quote_post') > 200 or item.get('3rd_quote_stack') > 200:
            cancel = True
        elif item.get('1st_quote_buyout') > 9000000  \
            or item.get('2nd_quote_buyout') > 9000000  \
            or item.get('3rd_quote_buyout') > 9000000:
            cancel = True
        else:
            cancel = False
        if not cancel:
            new_data.append(item)
    with open(goods_file_name, 'w') as fp:
        json.dump(new_data, fp, ensure_ascii=False)


def get_history_data(goods_file_name):
    with open(goods_file_name, 'r') as fp:
        data = json.load(fp)
    new_data = {}

    for item in data:
        for key in item.keys():
            if key not in new_data.keys():
                new_data[key] = []
            new_data.get(key).append(item.get(key))

    date_time = new_data.get('date&time')
    new_date_time = []
    for dt in date_time:
        dt = dt[11:17] + dt[18:21]
        new_date_time.append(dt)

    post1 = new_data.get('1st_quote_post')
    stack1 = new_data.get('1st_quote_stack')
    buyout1 = new_data.get('1st_quote_buyout')
    post2 = new_data.get('2nd_quote_post')
    stack2 = new_data.get('2nd_quote_stack')
    buyout2 = new_data.get('2nd_quote_buyout')
    post3 = new_data.get('3rd_quote_post')
    stack3 = new_data.get('3rd_quote_stack')
    buyout3 = new_data.get('3rd_quote_buyout')

    average_quote = []
    for i in range(len(post1)):
        item_quote = int((post1[i] * stack1[i] * buyout1[i] +
                              post2[i] * stack2[i] * buyout2[i] +
                              post3[i] * stack3[i] * buyout3[i]) /
                             (post1[i] * stack1[i] +
                              post2[i] * stack2[i] +
                              post3[i] * stack3[i])) / 100
        append = True
        if i != 0:
            if item_quote / average_quote[i - 1] > 5 or item_quote / average_quote[i - 1] < 0.2:
                append = False
            else:
                append = True
        if append:

            average_quote.append(item_quote)
    goods_name = goods_file_name.replace('scan_history\\', '')
    goods_name = goods_name.replace('_history.json', '')
    print(goods_name)
    final_data = {'date&time': new_date_time, goods_name: average_quote}
    return final_data, goods_name


filenames = []

for files in glob.glob("scan_history\\*.json"):
    filenames.append(files)

data_histories = []
goods_names = []
# filenames = filenames[7:8]
for file in filenames:
    history_clean(file)
    data_history, goods_name = get_history_data(file)
    df = pd.DataFrame.from_dict(data_history)
    data_histories.append(df)
    goods_names.append(goods_name)

print(data_histories)

# ax = plt.gca()


i = 0
for df in data_histories:
    # xs = df.get('date&time')
    # ys = df.get(goods_names[i])
    # plt.plot(xs, ys)
    df.plot(kind='line', x='date&time', y=goods_names[i])
    # df.plot(kind='line', x='date&time', y='average_quote', color='red', ax=ax)
    plt.savefig('scan_history\\' + goods_names[i] + 'quotes.png')
    i += 1
'''
axes.unicode_minus:False
font.family : sans-serif
font.sans-serif : SimHei, 
from matplotlib.font_manager import _rebuild
rebuild()
'''