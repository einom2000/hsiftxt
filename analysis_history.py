import keyboard, pyautogui,time
# while True:
#     if keyboard.is_pressed(' '):
#         print(pyautogui.position())
#         time.sleep(1)
#
import json
import matplotlib.pyplot as plt
from pandas.plotting import table
import pandas as pd
with open('scan_history\\阿昆达之噬_history.json', 'r') as fp:
    data = json.load(fp)
new_data = {}
for item in data:
    if 0 in item.values():
        cancel = True
    else:
        cancel = False
    if not cancel:
        for key in item.keys():
            if key not in new_data.keys():
                new_data[key] = []
            new_data.get(key).append(item.get(key))

date_time = new_data.get('date&time')
new_date_time =[]
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
    average_quote.append(int((post1[i] * stack1[i] * buyout1[i] +
                          post2[i] * stack2[i] * buyout2[i] +
                          post3[i] * stack3[i] * buyout3[i]) /
                         (post1[i] * stack1[i] +
                          post2[i] * stack2[i] +
                          post3[i] * stack3[i])) / 100
                         )

final_data = {'date&time': new_date_time, 'average_quote': average_quote}
df = pd.DataFrame.from_dict(final_data)
print(df)
ax = plt.gca()

df.plot(kind='line', x='date&time', y='average_quote', ax=ax)
# df.plot(kind='line', x='date&time', y='average_quote', color='red', ax=ax)

plt.show()
time.sleep(10)