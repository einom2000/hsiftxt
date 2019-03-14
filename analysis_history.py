import keyboard, pyautogui,time
import json
import matplotlib.pyplot as plt
import pandas as pd
import glob, numpy, sys
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
    # print(goods_file_name)
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
        append = item_quote
        if len(average_quote) >= 1:
            if item_quote / average_quote[-1] > 5 or item_quote / average_quote[-1] < 0.2:
                append = average_quote[-1]
            else:
                append = item_quote
        if append:
            average_quote.append(append)
    # change average_quote[] to percent quote:
    percent_quote = []
    max_quote = max(average_quote)
    min_quote = min(average_quote)
    average = (max_quote + min_quote) / 2
    for quote in average_quote:
        percent_quote.append(round(((quote - average) / average), 2))

    goods_name = goods_file_name.replace('scan_history\\', '')
    goods_name = goods_name.replace('_history.json', '')
    print(goods_name)
    final_data = {'date&time': new_date_time, goods_name: average_quote}
    final_per = {'date&time': new_date_time, goods_name: percent_quote}
    return final_data, goods_name, final_per




filenames = []

for files in glob.glob("scan_history\\*.json"):
    filenames.append(files)

df_histories = []
goods_names = []
percent_histories =[]

for file in filenames:
    history_clean(file)
    data_history, goods_name, percent_history = get_history_data(file)
    df = pd.DataFrame.from_dict(data_history)
    df_histories.append(df)
    goods_names.append(goods_name)
    percent_histories.append(percent_history)

i = 0
for df in df_histories:

    df.plot(kind='line', x='date&time', y=goods_names[i])
    plt.savefig('scan_history\\' + goods_names[i] + 'quotes.png', dpi=300)
    i += 1

# percentage whole chart
data_list = []
name_list = []
for per_dic in percent_histories:
        date_times_list = per_dic.get('date&time')
        per_quote_list = []
        for goods_name in goods_names:
            if goods_name in per_dic:
                name_list.append(goods_name)
                per_quote_list = per_dic.get(goods_name)
        dic = {}
        for d in range(len(date_times_list)):
            dic.update({d: per_quote_list[d]})
        data_list.append(dic)
dic = {}
for i in range(len(name_list)):
    dic.update({name_list[i]: data_list[i]})
df = pd.DataFrame(dic)
df.plot()
plt.savefig('scan_history\\' + 'whole_chart.png', dpi=600)

'''
axes.unicode_minus:False
font.family : sans-serif
font.sans-serif : SimHei, 
from matplotlib.font_manager import _rebuild
rebuild()
'''