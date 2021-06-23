import pandas as pd
import time

path = r'D:\工作_wxy\周报\流量数据\月度数据'
path_0 = r'D:\工作_wxy\周报\流量数据'
name = ['1月','2月','3月','4月','5月','6月-0622',]

def date_Str(str):
    str = str.replace('年', '-').replace('月', '-').replace('日', '')
    date1 = time.strptime(str, '%Y-%m-%d')
    date1 = time.strftime('%Y-%m-%d',date1)
    return date1

def csv_process(csv):
    sku_pv = pd.read_csv(csv)
    sku_pv['日期'] = sku_pv['日期'].apply(date_Str)
    sku_pv['日期'] = pd.to_datetime(sku_pv['日期'],format='%Y-%m-%d')
    sku_pv['产品 SKU'] = sku_pv['产品 SKU'].str.upper().apply(lambda x: x.strip())
    return sku_pv

for nm in name:
    csv_path = '%s\%s.csv'% ( path,nm )
    data = csv_process(csv_path)
    data.to_excel('%s\%s.xlsx'% ( path_0,nm ),index=None)
