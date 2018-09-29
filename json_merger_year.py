import pandas as pd
import numpy as np
import json
import os

root = 'data/cpcb/'

sites_arr = [118, 119, 124]#[114,117,301,1420,108,1560,104,103,118,1421,1422,116,106,1423,1424,109,1425,122,1561,115,1427,1426,1429,105,1428,1431,125,1563,107,124,1430,113,119,301,106,109]
for site in sites_arr:

    files = sorted(os.listdir(root))
    files = [i for i in files if 'site_'+str(site) in i]
    print(site, len(files))
    dfs = []

    for fil in files:
        print(fil)
        with open(root+fil) as f:
            d = json.load(f)

        print(d.keys())
        site = d['siteInfo']['siteId'][5:]
        print(site)
        assert(d['status']=='success')
        rec = d['tabularData']['bodyContent']
        df = pd.DataFrame.from_records(rec)
        # print(df.columns)
        if 'exceeding' in df.columns:
            df.drop('exceeding', axis=1, inplace=True)
        df['site'] = site
        # print(df)

        dfs.append(df)
    df = pd.concat(dfs)
    df.to_csv('data/Sitewise complete/'+site+'_complete.csv', index=False)
