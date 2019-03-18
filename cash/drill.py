import time
import os
from datetime import datetime, timedelta


def get_data_in_past_day(code, date):
    filename = ''
    if code[0] == '1':
        filename = 'C:\\new_ajzq_v6\\vipdoc\\sh\\lday\\sh' + code[1:] + '.day'
    elif code[0] == '0':
        filename = 'C:\\new_ajzq_v6\\vipdoc\\sz\\lday\\sz' + code[1:] + '.day'
    file_length_in_bytes = os.path.getsize(filename)
    with open(filename, mode='rb') as file:
        file.seek(-32, 2)
        for i in range(int(file_length_in_bytes / 32) - 1):
            dt = int.from_bytes(file.read(4), byteorder='little')
            if dt == int(date):
                opn_at = round(int.from_bytes(file.read(4), byteorder='little') / 100, 2)
                hghst = round(int.from_bytes(file.read(4), byteorder='little') / 100, 2)
                lwst = round(int.from_bytes(file.read(4), byteorder='little') / 100, 2)
                cls_at = round(int.from_bytes(file.read(4), byteorder='little') / 100, 2)
                return dt, opn_at, hghst, lwst, cls_at
            elif int(dt) < int(date):
                break
            else:
                file.seek(-36, 1)
        return 0, 0, 0, 0, 0


def get_history_from_a_certain_day(code, a_certain_date):
    i = 0
    datas = []
    while True:
        history_date = (datetime.now() - timedelta(days=i)).strftime('%Y%m%d')
        if int(str(history_date)) > int(a_certain_date):
            data = get_data_in_past_day(code, history_date)
            if data[0] != 0:
                datas.insert(0, data)
            else:
                pass
        else:
            break
        i += 1
    return datas


'''
history [(date, open, high, low, close), ....]
'''
history = (get_history_from_a_certain_day('0000001', '20190211'))
