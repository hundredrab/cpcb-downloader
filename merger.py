import os
import re
import pandas as pd

folder = 'data/2017'

files = os.listdir(folder)
csvs = [f for f in files if '.csv' == f[-4:]]
# print(csvs)

sheets = {}

for f in csvs:
    # print(f)
    search = re.search('site_(\d*)_?([a-zA-Z]*)_?\d\d\.csv', f, re.IGNORECASE)
    # print(search.group(1), search.group(2))
    if search is None:
        print(f, "is none")
        continue
    s_id = search.group(1)
    month = search.group(2)

    if s_id in sheets.keys():
        sheets[s_id].append(f)
    else:
        sheets[s_id] = [f]
import pprint

pprint.pprint(sheets)
for site in sheets.keys():
    df = []
    for file in sheets[site]:
        df.append(pd.read_csv(folder + '/' + file, index_col='From Date'))
        # print(df.head())
        # print("+")
    df = pd.concat(df)
    # print(df.tail())
    df.to_csv(site+'_complete_'+folder[-2:]+'.csv')
    print("___________________________________site " + site, 'len', len(sheets[site]), 'shape', df.shape)
