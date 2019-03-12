import json, keyboard,time

with open('scan_data.json', 'r') as fp:
    data = json.load(fp)

for goods in data:
    print(goods.get('item_name'), end='')
    print('snipper records:')
    keyboard.wait(' ')
    snipper_records = goods.get('item_buyout_history')
    # print(snipper_records)
    for snipper_record in snipper_records:
        date_time = snipper_record.get('date&time')
        threshold = snipper_record.get('threshold_price')
        threshold_pct = snipper_record.get('threshold_pct')
        buyout_price = snipper_record.get('buyout_price')
        buyout_stack = snipper_record.get('buyout_stack')
        buyout_post = snipper_record.get('buyout_post')
        next_quote = snipper_record.get('2nd_quotes')
        print('on ' + date_time)
        keyboard.wait(' ')
        print('with condition of ' + str(threshold) + ' and ' + str(threshold_pct))
        print('bought ' + str(buyout_post) + ' * ' + str(buyout_stack) + ' at ' + str(buyout_price / 100))
        print('the next quote is ' + str(next_quote / 100))
        keyboard.wait(' ')

