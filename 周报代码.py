import pandas as pd
from os import walk
import re
import time, datetime

# 合并易仓原始数据

def yc_trans(data,f):
    if f[:-30] == 'wayfairnew':
        platform_1 = 'wayfair'
    else:
        platform_1 = f[:-30]
    data['platform'] = platform_1
    data['年月'] = data['date_paid_platform'].apply(lambda x: x[:7])
    data['sku'] = data['sku'].str.upper().apply(lambda x: x.rstrip()).apply(lambda x: x.lstrip())
    data['refrence_no_sku'] = data['refrence_no'] + data['sku']
    data = data[['user_account', 'refrence_no_platform', 'refrence_no', 'consignee_country_code',
                 'refrence_no_warehouse', 'warehouse_code', 'currency', 'date_paid_platform', 'sku',
                 'refrence_no_sku', 'warehouse_sku', 'product_category', 'qty', 'unit_price', 'system_note','platform','年月']]
    return data

# 处理汇率

def pinjie(x, y):  # 定义拼接日期函数，整合汇率数据用
    if len(str(y)) == 1:
        z = str(x) + "-" + "0" + str(y)
    else:
        z = str(x) + "-" + str(y)
    return z

def er_trans(data_er,data_cy):
    data_er['年月'] = data_er.apply(lambda row: pinjie(row['YEAR'], row['MONTH']), axis=1)
    data_er.rename(columns={'CURRENCY': 'currency'}, inplace=True)
    data_er = data_er[['年月', 'currency', 'EXCHANGE_RATE']]  # 获取关键列
    data = pd.merge(data_cy, data_er, how='left', on=['年月', 'currency'])  # 合并数据集
    return data

# 主子单处理

def order_type(ot): # 根据备注中包含的关键词区分主单和子单
    pattern = re.compile(r'.*拆分后的子订单|订单合并|补发.*')
    if re.match(pattern, str(ot)):
        ot = '子单'
    else:
        ot = '主单'
    return ot

def main_order(data_yc_er):
    data_yc_er["主单or子单"] = data_yc_er['system_note'].apply(order_type)  # 区分主单子单
    data_yc_er['GMV'] = data_yc_er['EXCHANGE_RATE'] * data_yc_er['qty'] * data_yc_er['unit_price']
    print('总订单GMV: %s ,总行数: %d' % (data_yc_er['GMV'].sum(), len(data_yc_er)))
    data = data_yc_er[data_yc_er["主单or子单"] == "主单"]
    return data

# 仓库sku映射匹配

def wh_trans(data_wh,data_yc_er_m):
    data_wh = data_wh[['易仓SKU', '易仓仓库SKU', '是否为主sku数据']]
    data_wh = data_wh[(data_wh['是否为主sku数据'] == "否")]  # 筛选可映射的数据
    data_wh.drop_duplicates(subset=['易仓仓库SKU'], keep='first', inplace=True)
    data_wh['易仓仓库SKU'] = data_wh['易仓仓库SKU'].str.upper().apply(lambda x: x.strip())
    data_wh['易仓SKU'] = data_wh['易仓SKU'].str.upper().apply(lambda x: x.strip())
    data_wh.rename(columns={'易仓仓库SKU': 'sku', '易仓SKU': '主sku'}, inplace=True)
    data_wh.drop(['是否为主sku数据'],inplace=True,axis=1)
    data = pd.merge(data_yc_er_m, data_wh, how='left', on='sku')
    data['主sku'] = data['主sku'].fillna('dummy')
    return data

def sku(a, b):
    if str(a) == 'dummy':
        y = str(b)
    else:
        y = str(a)
    return y

def sku_trans(data):
    data['主sku2'] = data.apply(lambda row: sku(row['主sku'], row['sku']), axis=1)
    data.rename(columns={'sku': '原始sku','主sku2': 'sku'}, inplace=True)
    data.drop(['主sku'], axis=1, inplace=True)
    data['refrence_no_sku'] = data['refrence_no'] + data['sku']
    data['GMV'] = data['EXCHANGE_RATE'] * data['qty'] * data['unit_price']
    data["付款日期"] = data["date_paid_platform"].apply(lambda x: datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S").date())
    # data["付款日期"] = data["付款日期"].astype(str)
    data = data[['refrence_no', 'consignee_country_code', 'currency','sku', 'refrence_no_sku', 'qty', 'unit_price', 'platform', '年月', 'GMV', '付款日期', '原始sku']]
    return data

def pay_date_trans(str):
    date = datetime.datetime.strptime(str, '%Y-%m-%d').date()
    return date

# 处理homary数据

def hm_trans(hm_data,s_date,e_date):
    hm_data = hm_data[hm_data['付款时间'] != "无"]
    hm_data['SKU'] = hm_data['SKU'].astype(str)
    hm_data['SKU'] = hm_data['SKU'].str.replace('\'','')
    hm_data['付款日期'] = pd.to_datetime(hm_data['付款时间']).dt.date
    hm_data['年月'] = hm_data['付款日期'].apply(lambda x: str(x)[:7])
    hm_data['年月'] = hm_data['年月'].astype(str)
    hm_data['订单ID'] = hm_data['订单ID'].astype(str)
    hm_data['SKU'] = hm_data['SKU'].str.upper()
    hm_data['refrence_no_sku'] = hm_data['订单号'] + hm_data['SKU']
    hm_data = hm_data[(hm_data['付款日期'] >= s_date) & (hm_data['付款日期'] <= e_date)]
    hm_data['platform'] = 'hm'
    hm_data['SKU']= hm_data['SKU'].astype(str)
    hm_data = hm_data[['订单ID', '收货国家', '币种', 'SKU', 'refrence_no_sku', '订单数量', '单价', 'platform', '年月', '支付金额(CNY)', '付款日期']]
    hm_data['原始sku'] = hm_data['SKU']
    hm_data.rename(columns={
        '订单ID': 'refrence_no',
        '收货国家': 'consignee_country_code',
        '币种': 'currency',
        'SKU': 'sku',
        '订单数量': 'qty',
        '单价': 'unit_price',
        '支付金额(CNY)': 'GMV'},
        inplace=True)
    return hm_data


if __name__ == '__main__':
    start = '2021-07-15'
    end = '2021-07-19'
    s1 = '20210715'
    e1 = '20210718'
    s_date = datetime.datetime.strptime(start, '%Y-%m-%d').date()  # 筛选订单起始日期
    e_date = datetime.datetime.strptime(end, '%Y-%m-%d').date()  # 筛选订单终止日期
    path = r'D:\工作_wxy\周报\易仓原始数据\20210715-20210719'
    path_er = r'D:\工作_wxy\周报\周报维度表\%s\exchange_rate.xlsx' % e1
    path_wh = r'D:\工作_wxy\周报\周报维度表\%s\SKU映射关系(更新至20210429).xlsx' % e1

    data_lst = []
    data_er = pd.read_excel(path_er)
    data_wh = pd.read_excel(path_wh)

    for root,dirs,files in walk(path):
        for f in files:
            path_f = r'%s\%s' % (path, f)
            data = pd.read_excel(path_f)
            if 'homary' in f:
                data_hm = hm_trans(data,s_date,e_date) #如果是homary数据，用homary转换方式进行转换
            else:
                data = yc_trans(data, f) #易仓的数据，用易仓转换方式转换
                data_lst.append(data) #将易仓的各平台数据放入列表里

    data_yc = pd.concat(data_lst) #易仓各平台数据合并
    data_yc = data_yc[data_yc['user_account'] != 'Homary']
    data_yc_er = er_trans(data_er, data_yc) #易仓数据匹配汇率
    data_yc_er_m = main_order(data_yc_er) #判断主单子单
    data_yc_er_m_wh = wh_trans(data_wh, data_yc_er_m) #匹配仓库sku到主sku
    data_yc_er_m_wh_s = sku_trans(data_yc_er_m_wh) #匹配仓库sku到主sku
    data_yc_hm = pd.concat([data_hm, data_yc_er_m_wh_s]) #合并homary数据和易仓数据

    data2 = data_yc_hm
    data2.to_excel(r'D:\工作_wxy\周报\易仓原始数据\20210715-20210719\data_yc_hm.xlsx',index=None)
