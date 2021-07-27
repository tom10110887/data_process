import pandas as pd
import time

s = time.time()



def pms_data_trans(pms_data):
    pms_data['sku_up'] = ''
    pms_data['spu_up'] = ''
    pms_data['sku'] = pms_data['sku'].astype(str)
    pms_data['spu'] = pms_data['spu'].astype(str)
    pms_data['sku'] = pms_data['sku'].str.upper()
    pms_data['spu'] = pms_data['spu'].str.upper()
    pms_data = pms_data[['sku', 'spu', 'attr_combined_name', 'package_info', 'updated_package_info','sku_up','spu_up']]
    return pms_data

def update_data_trans(update_data):
    update_data["销售SKU"] = update_data["销售SKU"].astype(str).str.upper()
    update_data.rename(columns={'销售SKU':'sku',
                                '包裹内容物':'包裹内容物',
                                '包裹SKU':'wh_sku',
                                '长（最长边,cm）':'长',
                                '宽（中边，cm）':'宽',
                                '高（短边，cm）':'高',
                                '实重（kg）':'重'}, inplace=True)
    return update_data

def wh_data_trans(sku_wh):
    sku_wh['sales_sku'] = sku_wh['sales_sku'].str.upper()
    sku_wh['warehouse_sku'] = sku_wh['warehouse_sku'].str.upper()
    sku_wh['sku_up'] = ''
    sku_wh['sku_wh_up'] = ''
    sku_wh.rename(columns={'sales_sku':'sku','warehouse_sku':'wh_sku'}, inplace=True)
    return sku_wh

path = r'D:\工作_wxy\晓霞\更新包装尺寸0722.xlsx'

update_data = pd.read_excel(path, sheet_name='更新表')
sku_wh = pd.read_excel(path, sheet_name='sku关系')
pms_data = pd.read_excel(path, sheet_name='pms')

up_data0 = update_data_trans(update_data)
pms_data0 = pms_data_trans(pms_data)
wh_data0 = wh_data_trans(sku_wh)

data = pd.merge(up_data0, pms_data0, how='left', on='sku')
data.to_excel(r'D:\工作_wxy\晓霞\data0727.xlsx',index=None)

for index, row in data.iterrows():
    sku_1 = row[0]
    wh_sku_1 = row[2]
    for i,r in wh_data0.iterrows():
        sku_2 = r[0]
        wh_sku_2 = r[1]
        if sku_1 == sku_2:
            r[2] = '1'
        if wh_sku_1 == wh_sku_2:
            r[3] = '1'

wh_data0.to_excel(r'D:\工作_wxy\晓霞\wh_data0727.xlsx',index=None)

for index, row in data.iterrows():
    sku_1 = row[0]
    spu_1 = row[7]
    for i,r in pms_data0.iterrows():
        sku_2 = r[0]
        spu_2 = r[1]
        if sku_1 == sku_2:
            r[5] = '1'
        if spu_1 == spu_2:
            r[6] = '1'

pms_data0.to_excel(r'D:\工作_wxy\晓霞\pms_data0727.xlsx',index=None)

w_data = wh_data0[(wh_data0['sku_wh_up'] == '') & (wh_data0['sku_up'] == '1')]
w_data = pd.merge(w_data, pms_data0, how='left', on='sku')
p_data = pms_data0[(pms_data0['sku_up'] == '') & (pms_data0['spu_up'] == '1')]

p_data.to_excel(r'D:\工作_wxy\晓霞\p_data0727.xlsx',index=None)
w_data.to_excel(r'D:\工作_wxy\晓霞\w_data0727.xlsx',index=None)


e = time.time()

print(e - s)
