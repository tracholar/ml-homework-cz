# coding:utf-8
import sys
import pandas as pd

def timestamp2date(t):
    from datetime import datetime
    return datetime.fromtimestamp(t/1000).strftime('%Y-%m-%d')

if len(sys.argv) == 2:
    fname = sys.argv[1]
    df = pd.read_json(fname)

    column = df['data']['column']
    item = df['data']['item']

    dfx = pd.DataFrame({
        column[i] : [x[i] for x in item]
        for i in range(len(column))
    })
    if 'timestamp' in dfx.columns:
        dfx['date'] = dfx['timestamp'].map(lambda t : timestamp2date(t))

    name = fname.rsplit('.', 2)[0]
    dfx.to_excel(name + '.xlsx', index=False)