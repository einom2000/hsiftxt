import json
# scan_data=[
#             {
#             'item_name':'',
#             'item_threshold_price': 999999999,
#             'item_threshold_pct': 0,
#             'item_buyout_history':[{
#                                         'date&time': '',
#                                         'buyout_reason': '',
#                                         'threshold_price': 999999999,
#                                         'threshold_pct': 0,
#                                         'buyout_price': 0,
#                                         'buyout_stack': 0,
#                                         'buyout_post': 0,
#                                         '2nd_quotes': 0
#                                     }],
#             'item_price_history':[{
#                                         'date&time': '',
#                                         '1st_quote_post': 0,
#                                         '1st_quote_stack': 0,
#                                         '1st_quote_buyout': 0,
#                                         '2nd_quote_post': 0,
#                                         '2nd_quote_stack': 0,
#                                         '2nd_quote_buyout': 0,
#                                         '3rd_quote_post': 0,
#                                         '3rd_quote_stack': 0,
#                                         '3rd_quote_buyout': 0,
#                                         'snipper_flag': 'False'
#                                     }]
#             }]
scan_data = []

with open('scan_data.json', 'w') as fp:
    json.dump(scan_data, fp)

all_goods_names = ['暗月火酒', '暗月刃喉鱼']
all_goods_to_do = {'暗月火酒': [1, 19000, 5, 9000, 0.6, 2, 5],
                   '暗月刃喉鱼': [1, 1900, 100, 1500, 0.7, 3, 100]
                   }
snipper_list = [all_goods_names, all_goods_to_do]

with open('target_goods_list.json', 'w') as fp:
    json.dump(snipper_list, fp, ensure_ascii=False)