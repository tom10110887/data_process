import pandas as pd
import time

s = time.time()
now = time.ctime(s)
print(now)
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

path = r'D:\工作_wxy\商品中心\晓霞\更新包装尺寸0730.xlsx'
path0 = r'D:\工作_wxy\商品中心\晓霞\易仓尺寸.xlsx'

yc_data = pd.read_excel(path0)
yc_data['产品SKU'] = yc_data['产品SKU'].astype(str)

update_data = pd.read_excel(path, sheet_name='更新表')
sku_wh = pd.read_excel(path, sheet_name='sku关系')
pms_data = pd.read_excel(path, sheet_name='pms')

up_data0 = update_data_trans(update_data)
pms_data0 = pms_data_trans(pms_data)
wh_data0 = wh_data_trans(sku_wh)

data = pd.merge(up_data0, pms_data0, how='left', on='sku')

print('匹配pms')
num = 1

for index, row in data.iterrows():
    sku_1 = row[0]
    wh_sku_1 = row[2]
    if num % 100 == 0:
        print(num)
    for i,r in wh_data0.iterrows():
        sku_2 = r[0]
        wh_sku_2 = r[1]
        if sku_1 == sku_2:
            r[2] = '1'
        if wh_sku_1 == wh_sku_2:
            r[3] = '1'
        # if r[2] == '1' and r[3] == '1':
        #     break
    num += 1

num = 1
for index, row in data.iterrows():
    sku_1 = row[0]
    spu_1 = row[7]
    if num % 100 == 0:
        print(num)
    for i,r in pms_data0.iterrows():
        sku_2 = r[0]
        spu_2 = r[1]
        if sku_1 == sku_2:
            r[5] = '1'
        if spu_1 == spu_2:
            r[6] = '1'
        # if r[5] == '1' and r[6] == '1':
        #     break
    num += 1


data['来源'] = '更新表'
data = data[['来源', 'spu', 'sku', 'wh_sku', 'attr_combined_name', '包裹内容物', '长', '宽', '高', '重', 'updated_package_info', 'package_info']]

w_data = wh_data0[(wh_data0['sku_wh_up'] == '') & (wh_data0['sku_up'] == '1')]
p_data = pms_data0[(pms_data0['sku_up'] == '') & (pms_data0['spu_up'] == '1')]

print('匹配仓库')

if len(w_data) > 0:
    w_data['来源'] = 'SKU关系表'
    w_data['spu'] = ''
    w_data['attr_combined_name'] = ''
    w_data['包裹内容物'] = ''
    w_data['长'] = ''
    w_data['宽'] = ''
    w_data['高'] = ''
    w_data['重'] = ''
    w_data['updated_package_info'] = ''
    w_data['package_info'] = ''
    w_data = w_data[['来源', 'spu', 'sku', 'wh_sku', 'attr_combined_name', '包裹内容物', '长', '宽', '高', '重', 'updated_package_info', 'package_info']]

if len(p_data) > 0:
    p_data['来源'] = 'pms'
    p_data['wh_sku'] = ''
    p_data['attr_combined_name'] = ''
    p_data['包裹内容物'] = ''
    p_data['长'] = ''
    p_data['宽'] = ''
    p_data['高'] = ''
    p_data['重'] = ''
    p_data['updated_package_info'] = ''
    p_data['package_info'] = ''
    p_data = p_data[['来源', 'spu', 'sku', 'wh_sku', 'attr_combined_name', '包裹内容物', '长', '宽', '高', '重', 'updated_package_info', 'package_info']]


data_f = pd.concat([data,w_data,p_data])

print('更新尺寸')

for i, r in data_f.iterrows():
    if r[0] != '更新表':
        for x,y in pms_data0.iterrows():
            if r[2] == y[0]:
                r[1] = y[1]
                r[4] = y[2]
                r[10] = y[4]
                r[11] = y[3]
        for x,y in yc_data.iterrows():
            sku_1 = r[2]
            sku_2 = y[0]
            if sku_1 == sku_2:
                r[6] = y[12]
                r[7] = y[13]
                r[8] = y[14]
                r[9] = y[18]

data_f = data_f[['来源', 'spu', 'sku', 'wh_sku', 'attr_combined_name', '包裹内容物', '长', '宽', '高', '重', 'updated_package_info', 'package_info']]

data_f.to_excel(r'D:\工作_wxy\商品中心\晓霞\data0730-3.xlsx', index=None)

e = time.time()

print(e - s)





