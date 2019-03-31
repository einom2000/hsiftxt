import pandas as pd
import numpy as np

data =  pd.DataFrame(np.random.randn(5, 3), columns=['最低价', '紧盯量', '扫最高'])
#print (data)

def highlight_cols(s):
    color = 'grey'
    return 'background-color: %s' % color

data.style.applymap(highlight_cols, subset=pd.IndexSlice[:, ['B', 'C']])
print(data)