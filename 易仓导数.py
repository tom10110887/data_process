from selenium import webdriver
import time
from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

url = 'http://jyj.eccang.com/'

user_name = ''
user_password = ''

path = 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'

driver = webdriver.Chrome(path)
driver.maximize_window()
driver.get(url)
driver.find_element_by_name('userName').send_keys(user_name)
time.sleep(1)
driver.find_element_by_name('userPass').send_keys(user_password)
time.sleep(1)
driver.find_element_by_id('login').click()
time.sleep(5)
od_lst_link = driver.find_element_by_xpath("//*[@id='head']/div[2]/ul/li[1]").click()

time.sleep(2)

driver.switch_to.frame('iframe-container-0')
buttons = driver.find_element_by_xpath("//div/button[3]")

# print(buttons.get_attribute('outerHTML'))

buttons.click()

driver.switch_to.default_content()

time.sleep(2)


# driver.find_element_by_xpath("//a[text()='Amazon订单']").click()
driver.find_element_by_xpath('//*[@id="column"]/div[2]/ul[1]/li/a').click()
order1 = driver.find_element_by_xpath('//a[text()="订单管理"]')


print(order1)


time.sleep(1)

driver.find_element_by_xpath("//a[text()='Amazon订单']").click()

driver.switch_to.frame('iframe-container-38')

time.sleep(4)

cb = driver.find_element_by_xpath(".//span[text()='关闭']/..")
cbt = driver.find_element_by_xpath("/html/body/div[64]/div[3]/div/button")
print(cb.get_attribute('outerHTML'))
print(cbt.get_attribute('outerHTML'))



try:
    ActionChains(driver).move_to_element(driver.find_element_by_xpath("/html/body/div[64]/div[3]/div/button")).perform()
    # ActionChains(driver).move_to_element(driver.find_element_by_xpath(".//span[text()='关闭']/..")).perform()
    time.sleep(2)
    print('移动成功')
    driver.find_element_by_xpath("/html/body/div[64]/div[3]/div/button").click()
    # driver.find_element_by_xpath(".//span[text()='关闭']/..").click()
    print('成了！')
except:
    print('还是不行')

# try:
#     driver.find_element_by_xpath("//span[text()='关闭']/..").click()
# except:
#     print('点击失败')



# closebox.click()

# time.sleep(5)
#
# lst = [1,2,5,8,9,11]
#
# for num in lst:
#     selector = '#headmenu9 > div.topMenu_content > ul > ul > li:nth-child(%d) > a'% num
#     # selector = r'#headmenu9 > div.topMenu_content > ul > ul > li:nth-child(1) > a'
#     print(selector)
#     platefrom_order = driver.find_element_by_css_selector(selector)
#     platefrom_order.click()


# //*[@id="headmenu9"]/div[2]/ul/ul/li[1]/a


time.sleep(5)
driver.close()



