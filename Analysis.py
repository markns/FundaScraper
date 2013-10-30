import glob

__author__ = 'markns'

DATA_DIR = "/Volumes/Users/markns/Google Drive/Data/"

files = glob.glob(DATA_DIR + '????-??-??-amsterdam.csv')

print files

import pandas as pd


c = 1

for csv in files:
    print csv
    df = pd.read_csv(csv)
    # print df.loc[:, ['Vraagprijs']].head()

    if c == 1:
        c += 1
        continue

    stk_list = ['West', 'Zuid']

    print df[df['Stadsdeel'].isin(stk_list)].loc[:, ['Vraagprijs']].mean()
    print df.loc[:, ['Vraagprijs']].mean()



