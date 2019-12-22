import pandas as pd
import os
from os import listdir
from os.path import isfile, join
import re
data= {}
csvfiles = [f for f in listdir(os.path.dirname(os.path.realpath(__file__))) if isfile(join(os.path.dirname(os.path.realpath(__file__)), f)) and re.search(r'\d\.csv$', f)]
for f in csvfiles:
    x = pd.read_csv('./' + f, index_col=False)
    for col in x.columns[1:]:
        data[col+'_'+f]=eval(x[col][0])
for a, b in data.items():
    print('filename:',a,'hrefs:',str(len(b)))
pd.DataFrame.from_dict(data, orient='index').transpose().to_csv (r'./Summary.csv', index = None)