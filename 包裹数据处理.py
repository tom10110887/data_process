import pandas as pd
import time

s = time.time()

path = r'D:\工作_wxy\晓霞\更新包装尺寸0722.xlsx'

update_data = pd.read_excel(path,sheet_name='更新表')
sku_wh = pd.read_excel(path,sheet_name='sku关系')
pms_data = pd.read_excel(path,sheet_name='pms')

pms_data = pms_data[['sku','spu','attr_combined_name','package_info','updated_package_info']]
pms_data['sku'] = pms_data['sku'].str.upper()
pms_data['spu'] = pms_data['spu'].str.upper()
update_data["销售SKU"] = update_data["销售SKU"].astype(str).str.upper()
update_data.rename(columns={'销售SKU':'sku',
                            '包裹内容物':'包裹内容物',
                            '包裹SKU':'wh_sku',
                            '长（最长边,cm）':'长',
                            '宽（中边，cm）':'宽',
                            '高（短边，cm）':'高',
                            '实重（kg）':'重'},inplace=True)
sku_wh['sales_sku'] = sku_wh['sales_sku'].str.upper()
sku_wh['warehouse_sku'] = sku_wh['warehouse_sku'].str.upper()
sku_wh.rename(columns={'sales_sku':'sku','warehouse_sku':'wh_sku'}, inplace=True)
sku_wh['sku_up'] = ''
sku_wh['sku_wh_up'] = ''

data = pd.merge(update_data,pms_data,how='left',on='sku')

for j in range(len(sku_wh)):
    data_wh = sku_wh.iloc[j].values.tolist()
    for i in range(len(sku_data)):
        data = sku_data.iloc[i].values.tolist()
        if data[0] == data_wh[0]:
            sku_wh.iloc[j,2] = '1'
        if data[1] == data_wh[1]:
            sku_wh.iloc[j,3] = '1'

data_r = sku_wh[(sku_wh['sku_up'] == '1') & (sku_wh['sku_wh_up'] == '')]



e = time.time()


data3.to_excel(r'D:\工作_wxy\晓霞\test2.xlsx',index=None)

print(e - s)
