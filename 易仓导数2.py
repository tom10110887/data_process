from selenium import webdriver
import time
from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

url = 'http://jyj.eccang.com/'

user_name = ''
user_password = ''
start = '2021-07-12'
end = '2021-07-14'

path = 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'

driver = webdriver.Chrome(path)
driver.maximize_window()
driver.get(url)

try:
    driver.find_element_by_name('userName').send_keys(user_name)
    time.sleep(1)
    driver.find_element_by_name('userPass').send_keys(user_password)
    time.sleep(1)
    driver.find_element_by_id('login').click()
    time.sleep(5)
    print('登陆成功')
except:
    print('登录失败')

try:
    od_lst_link = driver.find_element_by_xpath("//li/a[text()='订单管理系统']/..").click()
    print('成功进入订单管理系统')
except:
    print('订单管理系统进入失败')

time.sleep(2)

try:
    driver.switch_to.frame('iframe-container-0')
    buttons2 = driver.find_element_by_xpath("//span[contains(text(),'我知道了，关闭')]/..")
    time.sleep(1)
    buttons2.click()
    print('成功关闭弹窗')
except:
    print('订单管理系统弹窗关闭失败')

driver.switch_to.default_content()

time.sleep(2)

def order_manegament(driver):
    order1 = driver.find_element_by_xpath('//a[text()="订单管理"]')
    time.sleep(1)
    order1.click()
    print('点击订单管理按钮成功')
    time.sleep(1)

od_wb_lst = ['Amazon订单','eBay订单','Walmart订单','Wayfairnew订单','B2C订单']

try:
    order_manegament(driver)
    for wb in od_wb_lst:
        driver.find_element_by_xpath("//a[text()='%s']"% wb).click()
        print('点击%s成功'% wb)
        time.sleep(1)
except:
    print('点击订单失败')


wb_dic = {'amazon':'Amazon订单','ebay':'eBay订单','walmart':'Walmart订单','wayfairnew':'Wayfairnew订单','b2c':'B2C订单'}

meau = driver.find_element_by_xpath("//div[@class='logo2']")

time.sleep(2)

ActionChains(driver).move_to_element(meau)
print('移动到主页按钮成功')

ActionChains(driver).move_by_offset(960, 0).click().perform()
ActionChains(driver).move_by_offset(-960, 0).perform()

time.sleep(2)

for key,value in wb_dic.items():
    print(key,value)

    title_bt = "//a[@title=\'%s\']"% value

    bt = driver.find_element_by_xpath(title_bt)

    time.sleep(3)

    bt.click()

    driver.switch_to.frame(driver.find_element_by_xpath("//iframe[contains(@src,\'%s\')]"% key))
    time.sleep(1)

    if key == 'amazon':
        driver.find_element_by_xpath("//span[@id='ui-id-52']/../button").click()
    elif key == 'ebay':
        driver.find_element_by_xpath("//span[@id='ui-id-51']/../button").click()

    time.sleep(2)
    # 展开高级搜索

    if key in ['amazon','ebay','walmart']:
        more_con = driver.find_element_by_xpath("//span[text()='展开更多订单条件']/..")
    else:
        more_con = driver.find_element_by_xpath("//a[text()='高级搜索']")

    time.sleep(1)

    more_con.click()

    time.sleep(1)
    if key == 'amazon':
        driver.find_element_by_xpath('//input[@id="createDateFrom"]').send_keys('%s 00:00:00'% start)
        driver.find_element_by_xpath('//input[@id="createDateEnd"]').send_keys('%s 00:00:00'% end)
    else:
        driver.find_element_by_xpath('//input[@id="payDateFrom"]').send_keys('%s 00:00:00' % start)
        driver.find_element_by_xpath('//input[@id="payDateEnd"]').send_keys('%s 00:00:00' % end)

    time.sleep(2)

    driver.find_element_by_xpath('//a[@id="last_six_months"]').click()

    time.sleep(2)

    for i in range(1,7):
        ActionChains(driver).key_down(Keys.DOWN).perform()

    time.sleep(1)
    print('下拉成功')

    #点击按条件导出

    if key in ['amazon','ebay','walmart']:
        dld = driver.find_element_by_xpath('//div[@id="fix_header_content"]/descendant::span[text()="导入导出"]')
        ActionChains(driver).move_to_element(dld).perform()
        print('导入导出悬停成功')
        time.sleep(1)
        dld_con = driver.find_element_by_xpath("//div[@id='fix_header_content']/descendant::input[@value='按条件导出']")
        time.sleep(2)
        ActionChains(driver).move_to_element(dld_con).perform()
        print("移动到条件导出按钮成功！！")
        export = driver.find_element_by_xpath("//div[@id='fix_header_content']/descendant::input[@value='按条件导出']")
        time.sleep(2)
        export.click()
        print("按条件导出点击成功！！！")
    else:
        dld_con = driver.find_element_by_xpath("//div[@id='fix_header_content']/descendant::input[@value='按条件导出']")
        time.sleep(1)
        dld_con.click()

    time.sleep(1)

    cnt = driver.find_element_by_xpath("//div[@class='pageTotal']/b[1]").text
    print('共查询到 %s 条数据'%cnt)

    if cnt != '0':
        driver.find_element_by_xpath('//p[contains(text(),"确定按照搜索条件导出订单")]/../../div/div/button').click()
        print("订单导出成功！！！")
    else:
        print("该时间段内%s平台无订单"%key)

    handles = driver.window_handles
    driver.switch_to.window(handles[0])

    time.sleep(1)

    driver.switch_to.default_content()


time.sleep(5)
driver.close()
