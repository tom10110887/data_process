import pandas as pd
import time
import datetime

# 缺货小工具字段处理

def xgj_data_trans(xgj_data):
    data = xgj_data[['订单付款日期','平台','易仓单号','订单号','商城ETA','国家','审单目的仓','销售SKU','仓库SKU','数量','状态匹配','状态匹配数量','首次预计到客时间','预计到客时间','调拨单','跟踪单号','采购单号','客服跟单备注']]
    data = data[data.平台.isin(['HM','Homary'])] # 筛选只要homary平台的
    data['销售SKU'] = data['销售SKU'].str.upper()
    data['仓库SKU'] = data['仓库SKU'].str.upper()
    data['调拨单'] = data['调拨单'].str.strip()
    data['调拨单'] = data['调拨单'].str.split(' ')
    data['跟踪单号'] = data['跟踪单号'].str.replace('柜|号|：|: |:|新|仓|泽|西|暂无','')
    data['跟踪单号'] = data['跟踪单号'].str.strip()
    data['跟踪单号'] = data['跟踪单号'].str.split(' ')
    data['采购单号'] = data['采购单号'].str.strip()
    data['采购单号'] = data['采购单号'].str.split(' ')

    data.rename(columns={'订单付款日期':'pay_date',
                        '平台':'platform',
                        '易仓单号':'yc_order',
                        '订单号':'order',
                        '商城ETA':'ETA_mall',
                        '国家':'country',
                        '审单目的仓':'target_warehouse',
                        '销售SKU':'sku',
                        '仓库SKU':'wh_sku',
                        '数量':'amount',
                        '状态匹配':'lastest_status',
                        '状态匹配数量':'lastest_status_amount',
                        '首次预计到客时间':'first_eta_date_xgj',
                        '预计到客时间':'eta_date_xgj',
                        '采购单号':'purchase_order',
                        '调拨单':'delivery_num',
                        '跟踪单号':'cabinet_num',
                        '客服跟单备注':'cs_note'},inplace=True)
    return data

# 易仓数据处理

def yc_data_trans(yc_data):
    yc_data['产品代码'] = yc_data['产品代码'].str.upper()
    yc_data['产品代码'] = yc_data['产品代码'].str.strip()
    data = yc_data[['订单系统参考号', '产品代码', '数量', '参考号', '订单状态', '订单号', '出货时间']]
    data.rename(columns={'订单系统参考号': 'order', '产品代码': 'wh_sku', '数量': 'status_amount', '参考号': 'yc_order',
                         '订单状态': 'yc_order_status', '订单号': 'yc_MT_order', '出货时间': 'ship_date'}, inplace=True)
    return data

# 管理表处理

def m_data_trans(data_manage):
    data_manage['销售SKU'] = data_manage['销售SKU'].str.strip()
    data_manage['销售SKU'] = data_manage['销售SKU'].str.upper()
    data_manage['仓库SKU'] = data_manage['仓库SKU'].str.strip()
    data_manage['仓库SKU'] = data_manage['仓库SKU'].str.upper()
    data_manage.rename(columns={
        '订单付款日期': 'pay_date',
        '平台': 'platform',
        '易仓单号': 'yc_order',
        '订单号': 'order',
        '商城ETA': 'ETA_mall',
        '国家': 'country',
        '审单目的仓': 'target_warehouse',
        '销售SKU': 'sku',
        '仓库SKU': 'wh_sku',
        '数量': 'amount',
        '最新状态': 'lastest_status',
        '最新状态数量': 'lastest_status_amount',
        '首次预计到客时间': 'first_eta_date_xgj',
        '预计到客时间': 'eta_date_xgj',
        '采购单号': 'purchase_order',
        '调拨单': 'delivery_num',
        '海运柜号': 'cabinet_num',
        '客服跟单备注': 'cs_note',
        '派送时间（天）': 'delivery_days',
        'ETA_DATE': 'expected_arrive_date',
        '履约期所剩天数': 'remain_days',
        '易仓订单状态': 'yc_order_status',
        '当前状态': 'status',
        '状态匹配数量': 'status_amount',
        '状态轨迹（含当前状态）': 'status_history',
        '申购未下单匹配日期': 'purchase_pre_date',
        '申购作业天数': 'purchase_pre_status_days',
        '待发海运匹配日期': 'sea_trans_pre_date',
        '待发海运作业天数': 'sea_trans_pre_status_days',
        '佛山备货匹配日期': 'fs_pre_date',
        '佛山备货作业天数': 'fs_pre_status_days',
        '待发货日期': 'pre_ship_date',
        '出货日期': 'ship_date'}, inplace=True)
    return data_manage

# sku关系表处理

def re_data_trans(re_data):
    re_data = pd.read_csv(path_relation, converters={'平台销售SKU': str, '仓库SKU': str}, encoding='gbk')
    re_data['平台销售SKU'] = re_data['平台销售SKU'].str.upper()
    re_data['仓库SKU'] = re_data['仓库SKU'].str.upper()
    re_data = re_data[['平台销售SKU', '仓库SKU']]
    re_data.rename(columns={'平台销售SKU': 'sku', '仓库SKU': 'wh_sku'}, inplace=True)
    return re_data

def cancel_data_trans(hm_cancel_data,yc_cancel_data):
    hm_cancel_data['SKU'] = hm_cancel_data['SKU'].str.upper()
    hm_cancel_data['SKU'] = hm_cancel_data['SKU'].str.replace('\'', '')
    yc_cancel_data['SKU'] = yc_cancel_data['SKU'].str.upper()
    hm_cancel_data = hm_cancel_data[['参考号(商城订单号)', 'SKU', '退款数量', '处理方案']]
    yc_cancel_data = yc_cancel_data[['参考号', 'SKU', '退款数量', '处理方案']]
    hm_cancel_data.rename(columns={'参考号(商城订单号)': 'order', 'SKU': 'sku', '退款数量':'status_amount', '处理方案':'status'}, inplace=True)
    yc_cancel_data.rename(columns={'参考号': 'order', 'SKU': 'sku', '退款数量': 'status_amount', '处理方案': 'status'}, inplace=True)
    cancel_data = pd.concat([yc_cancel_data, hm_cancel_data])
    return cancel_data


root = r'D:\工作_wxy\运营中心\缺货跟踪'
path_xgj = r'%s\7.30 缺货小工具.xlsx' % root
path_yc = r'%s\易仓报表.xlsx' % root
path_manage = r'%s\缺货订单跟踪模板.xlsx' % root
path_relation = r'%s\sku-relation-1627895657.csv' % root
path_hm_cancel = r'%s\homary 后台取消订单.xlsx' % root
path_yc_cancel = r'%s\易仓取消订单717-723.xlsx' % root

xgj_data = pd.read_excel(path_xgj,converters={'易仓单号': str, '订单号': str, '销售SKU': str, '仓库SKU': str})
yc_data = pd.read_excel(path_yc, converters={'订单系统参考号': str,'产品代码': str, '参考号': str, '订单号': str})
data_manage = pd.read_excel(path_manage, converters={'易仓单号': str,'订单号': str, '销售SKU': str, '仓库SKU': str})
re_data = pd.read_csv(path_relation, converters={'平台销售SKU': str, '仓库SKU': str}, encoding='gbk')
hm_cancel_data = pd.read_excel(path_hm_cancel, converters={'SKU': str, '参考号(商城订单号)': str})
yc_cancel_data = pd.read_excel(path_yc_cancel, converters={'SKU': str, '参考号': str})

xgj_data = xgj_data_trans(xgj_data)
yc_data = yc_data_trans(yc_data)
data_manage = m_data_trans(data_manage)
re_data = re_data_trans(re_data)
cancel_data = cancel_data_trans(hm_cancel_data, yc_cancel_data)

xgj_data.to_excel(r'%s\xgj_data_0802.xlsx' % root,index=None)
yc_data.to_excel(r'%s\yc_data_0802.xlsx' % root,index=None)
data_manage.to_excel(r'%s\m_data_0802.xlsx' % root,index=None)
re_data.to_excel(r'%s\re_data_0802.xlsx' % root,index=None)
cancel_data.to_excel(r'%s\cancel_data_0802.xlsx' % root, index=None)

