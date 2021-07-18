import pandas as pd
start = '2021-07-15'
end = '2021-07-18'
path = r'C:\Users\XIANGYAN\Desktop\amazon_order_export_210718135621.csv'

data = pd.read_csv(path)

def cut_str(str):
    a = str[2:-1]
    return a


for i in data:
    data[i] = data[i].astype(str)
    data[i] = data[i].apply(cut_str)
    try:
        data[i] = data[i].astype(float)
        print('%s 能转换成数字\n'%i)
    except:
        print('%s 不能转换成数字\n'%i)

s1 = start.replace('-','')
e1 = end.replace('-','')

data.to_excel(r'C:\Users\XIANGYAN\Desktop\amazon_order(%s-%s).xlsx'%(s1,e1))



