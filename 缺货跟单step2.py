import pandas as pd
import time
import datetime
import re

# 把商场ETA转化为天数
def convert_to_days(str):
    if type(str) != float:
        if 'weeks' in str or 'Wochen' in str or 'semaines' in str or 'semanas' in str:
            pattern = re.compile(r'.*(?=weeks|Wochen|semaines|semanas)')
            result1 = re.findall(pattern, str)[0]
            result = result1.split('-')
            result = result[-1]
            days = int(result) * 7
        elif ('days' in str or 'Tage' in str or 'días' in str or 'jours' in str) and 'to' not in str:
            pattern = re.compile(r'.*(?=days|Tage|días|jours)')
            result1 = re.findall(pattern, str)[0]
            result = result1.split('-')
            days = result[-1]
            days = int(days)
        elif 'business' in str:
            pattern = re.compile(r'.*(?= business.*)')
            result1 = re.findall(pattern, str)[0]
            result = result1.split(' to ')
            days = result[-1]
            days = int(days)
        else:
            days = ''
    else:
        days = ''
    return days

def eta_date(pay_date, d_days):
    if d_days != '':
        pay_date = datetime.datetime.strptime(pay_date[:10], "%Y-%m-%d")
        td = datetime.timedelta(days=d_days)
        eta_date1 = (pay_date + td).date()
        eta_date = (pay_date + td).strftime('%Y-%m-%d')
        remain_days = eta_date1 - datetime.date.today()
        remain_days = remain_days.days
    else:
        eta_date = ''
        remain_days = ''
    return [eta_date, remain_days]

def status_days(status_date):
    if status_date != 'NANA':
        # status_date = status_date.strftime('%Y-%m-%d')
        status_date = datetime.datetime.strptime(status_date, '%Y-%m-%d').date()
        days = datetime.date.today() - status_date
    else:
        days = ''
    return days

root = r'D:\工作_wxy\运营中心\缺货跟踪'
path = r'%s\处理缺货订单11.xlsx' % root
data = pd.read_excel(path)
data['delivery_days'] = data['ETA_mall'].apply(convert_to_days)
data['ETA_DATE'] = data.apply(lambda row: eta_date(row['pay_date'], row['delivery_days'])[0], axis=1)
data['remain_days'] = data.apply(lambda row: eta_date(row['pay_date'], row['delivery_days'])[1], axis=1)
for nm in ['purchase','sea_trans','fs']:
    data['%s_pre_date'% nm] = data['%s_pre_date'% nm].fillna('NANA')
    data['%s_pre_status_days'% nm] = data['%s_pre_date'% nm].apply(status_days)
    data['%s_pre_date'% nm] = data['%s_pre_date'% nm].astype(str)
    data['%s_pre_date'% nm] = data['%s_pre_date'% nm].str.replace('NANA','')



data.to_excel(r'%s\data_0804_6.xlsx' % root, index=None, sheet_name='订单管理总表')
