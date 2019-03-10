# import csv
#
# with open('tempcsv.txt') as csv_file:
#     csv_reader = csv.reader(csv_file, delimiter=',')
#     line_count = 0
#     for row in csv_reader:
#         if line_count == 0:
#             print(f'Column names are {", ".join(row)}')
#             line_count += 1
#         else:
#             print(f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
#             line_count += 1
#     print(f'Processed {line_count} lines.')

import json

filename = '这是个测试'
data = "123123123还是个测试"
with open('scan_history\\' + filename + '.json', 'w') as fp:
     json.dump([], fp, ensure_ascii=False)
