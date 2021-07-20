import pandas as pd
from os import walk
from os import mkdir

start = '2021-07-15'
end = '2021-07-18'
s1 = start.replace('-','')
e1 = end.replace('-','')
path = r'D:\工作_wxy\周报\易仓原始数据'
path_src = r'D:\工作_wxy\周报\易仓原始数据\csv文件'
path_result = '%s\%s-%s' % (path, s1, e1)
mkdir(path_result,0o0755)


def cut_str(str):
    a = str[2:-1]
    return a

def yc_data_process(data):
    for i in data:
        data[i] = data[i].astype(str)
        data[i] = data[i].apply(cut_str)
        try:
            data[i] = data[i].astype(float)
        except:
            pass
    return data

def hm_data_process(data):
    data['SKU'].str
    data = data[['订单ID', '下单时间', '付款时间', '订单号', '支付单号', 'SKU', '订单数量', '单价（当前币种）', '支付金额', '支付金额(CNY)', '币种', '订单状态',
         '发货时间', '取消原因', '站点', '收货国家', '收货省', '收货城市', '邮编', '邮箱', '姓名', '姓氏', '支付类型', '优惠领取ID', '优惠券别名', '优惠金额',
         '用户类型']]
    return data


for root, dirs, files in walk(path_src):
    for f in files:
        data = pd.read_csv('%s\%s' % (path_src, f))
        if 'order_export' in f:
            data = yc_data_process(data)
            nm = f[:-24]
            data.to_excel('%s\%s(%s-%s).xlsx'%(path_result, nm, s1, e1), index=None)
        else:
            data = hm_data_process(data)
            data.to_excel('%s\homary_order(%s-%s).xlsx' % (path_result, s1, e1), index=None)
