from selenium import webdriver
import time
from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

url = 'http://jyj.eccang.com/'

user_name = 'shuju10'
user_password = 'bmwxy123456*'
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
    buttons = driver.find_element_by_xpath("//div/button[3]")
    buttons2 = driver.find_element_by_xpath("//span[contains(text(),'我知道了，关闭')]/..")
    time.sleep(1)
    buttons2.click()
    print('成功关闭弹窗')
except:
    print('订单管理系统弹窗关闭失败')

driver.switch_to.default_content()

time.sleep(2)

try:
    order1 = driver.find_element_by_xpath('//a[text()="订单管理"]')
    order1.click()
    print('点击订单管理按钮成功')
except:
    print('点击订单管理失败')

time.sleep(1)

try:
    driver.find_element_by_xpath("//a[text()='Amazon订单']").click()
    print('点击亚马逊订单成功')
except:
    print('点击亚马逊订单失败')

driver.switch_to.frame('iframe-container-38')

time.sleep(4)

try:
    ActionChains(driver).move_to_element(driver.find_element_by_xpath("//td[text()='Tips']/../../../../../div/div/button")).perform()
    time.sleep(2)
    print('关闭亚马逊弹窗成功')
    driver.find_element_by_xpath("//div[64]/div/button").click()
except:
    print('还是不行')


more_con = driver.find_element_by_xpath("//span[text()='展开更多订单条件']/..")

time.sleep(2)

more_con.click()

try:
    driver.find_element_by_xpath('//input[@id="createDateFrom"]').send_keys('%s 00:00:00'% start)
    driver.find_element_by_xpath('//input[@id="createDateEnd"]').send_keys('%s 00:00:00'% end)
    time.sleep(2)
    driver.find_element_by_xpath('//a[@id="last_six_months"]').click()
    time.sleep(2)
except:
    print("输入错误")


try:
    for i in range(1,7):
        ActionChains(driver).key_down(Keys.DOWN).perform()

    time.sleep(2)
    ActionChains(driver).move_to_element(driver.find_element_by_xpath('//div[@id="fix_header_content"]/descendant::span[text()="导入导出"]')).perform()
    time.sleep(1)
    print("导入导出悬停成功")
    time.sleep(2)
except:
    print('导入导出悬停失败')

try:
    export = driver.find_element_by_xpath("//div[@id='fix_header_content']/descendant::input[@value='按条件导出']")
    time.sleep(2)
    ActionChains(driver).move_to_element(export).perform()
    print("移动到条件导出按钮成功！！")
    export_2 = driver.find_element_by_xpath("//div[@id='fix_header_content']/descendant::input[@value='按条件导出']")
    time.sleep(2)
    export_2.click()
    print("按条件导出点击成功！！！")
except:
    print('按条件导出点击失败')

time.sleep(2)

try:
    driver.find_element_by_xpath('//p[contains(text(),"确定按照搜索条件导出订单")]/../../div/div/button').click()
    print("订单导出成功！！！")
except:
    print('按搜索条件导出点击失败')


time.sleep(5)
driver.close()
