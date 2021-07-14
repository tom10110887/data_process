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
od_lst_link = driver.find_element_by_xpath("//li/a[text()='订单管理系统']/..").click()


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
cbt = driver.find_element_by_xpath('//button[@type="button" and @role="button"]')
print(cb.get_attribute('outerHTML'))
print(cbt.get_attribute('outerHTML'))


time.sleep(2)
try:
    # ActionChains(driver).move_to_element(driver.find_element_by_xpath("/html/body/div[64]/div[3]/div/button")).perform()
    ActionChains(driver).move_to_element(driver.find_element_by_xpath("//td[text()='Tips']/../../../../../div/div/button")).perform()
    # ActionChains(driver).move_to_element(driver.find_element_by_xpath('//div[64]/div/button')).perform()
    time.sleep(2)
    print('移动成功')
    driver.find_element_by_xpath("//div[64]/div/button").click()
    # driver.find_element_by_xpath(".//span[text()='关闭']/..").click()
    print('成了！')
except:
    print('还是不行')

# try:
#     driver.find_element_by_xpath("//span[text()='关闭']/..").click()
# except:
#     print('点击失败')

more_con = driver.find_element_by_xpath("//span[text()='展开更多订单条件']/..")
time.sleep(2)

more_con.click()
try:
    driver.find_element_by_xpath('//input[@id="createDateFrom"]').send_keys('2021-07-05 00:00:00')
    driver.find_element_by_xpath('//input[@id="createDateEnd"]').send_keys('2021-07-11 00:00:00')
    time.sleep(2)
    driver.find_element_by_xpath('//a[@id="last_six_months"]').click()
    time.sleep(2)
except:
    print("输入错误")


try:
    ActionChains(driver).move_to_element(driver.find_element_by_xpath('//span[text()="导入导出"]')).perform()
    time.sleep(1)
    # driver.find_element_by_xpath('//input[@value="按条件导出"]/..').click()
    print("牛蛙！")
    ActionChains(driver).key_down(Keys.DOWN).perform()
    ActionChains(driver).key_down(Keys.DOWN).perform()
    ActionChains(driver).key_down(Keys.DOWN).perform()
    ActionChains(driver).key_down(Keys.DOWN).perform()
    time.sleep(2)
    ActionChains(driver).move_to_element(driver.find_element_by_xpath('//input[@value="按条件导出"]')).perform()
    print("牛蛙！！")
    driver.find_element_by_xpath('//input[@value="按条件导出"]').click()
    print("牛蛙！！！")
    time.sleep(2)
    driver.find_element_by_xpath('//p[contains(text(),"确定按照搜索条件导出订单")]/../../div/div/button').click()
    print("太牛了蛙！！！")
except:
    print('导出按钮点击失败')
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



