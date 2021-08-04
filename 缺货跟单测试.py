import pandas as pd
import time
import datetime
import re

root = r'D:\工作_wxy\运营中心\缺货跟踪'
path = r'%s\data_0804_6.xlsx' % root
data = pd.read_excel(path)

def status_his_up(status,lastest,status_num,lastest_num, status_his):
    if status_his is None or status_his == '':
        if lastest is None or lastest == '':
            if status is None or status == '':
                return None
            else:
                new_status = status + '*' + str(status_num)
                return new_status
        else:
            new_status = lastest + '*' + str(lastest_num)
            return new_status
    if status == lastest and status_num == lastest_num:
        return None
    else:
        new_status = lastest + '*' + str(lastest_num)
        return new_status

def his_update(status,lastest,status_num,lastest_num, status_his):
    if status_his is None or status_his == '':
        his = status_his_up(status,lastest,status_num,lastest_num, status_his)
        return his
    else:
        new_his = status_his_up(status,lastest,status_num,lastest_num, status_his)
        if new_his is not None:
            his = status_his + '|' + new_his
        else:
            his = status_his
        return his

data['status_history'] = data.apply(lambda row: his_update(row['status'], row['lastest_status'], row['status_amount'], row['lastest_status_amount'], row['status_history']), axis=1)


data.to_excel(r'%s\data_0804_6_1.xlsx' % root, index=None, sheet_name='取消订单')
