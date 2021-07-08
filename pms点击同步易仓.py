from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time


url_pms = 'https://pms.popicorns.com/module/'
user_nm_yc = 'xiaolu'
password_yc = '888lujiaxin'

driver = webdriver.Chrome()
driver.maximize_window()
driver.get(url_pms)

driver.find_element_by_xpath(".//input[@type='text']").send_keys(user_nm_yc)

time.sleep(1)
driver.find_element_by_xpath(".//input[@type='password']").send_keys(password_yc)
time.sleep(1)
driver.find_element_by_xpath(".//button[@type='button']").click()
time.sleep(3)
driver.get('https://pms.popicorns.com/module/pms/commodityManagement/commodityConsole')
time.sleep(12)

print('done')

def click_yc(num):
    try:
        driver.find_element_by_xpath("//*[@id='tables']/div[4]/div[2]/table/tbody/tr[%d]/td[14]/div/div/p[4]" % num).click()
        return False
    except:
        return True

for k in range(1,100):
    for num in range(1,11):
        print(num)
        while click_yc(num):
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            ActionChains(driver).move_by_offset(960, 360).click().perform()
            ActionChains(driver).key_down(Keys.DOWN).perform()
            ActionChains(driver).move_by_offset(-960, -360).perform()
        # for j in range(1,4):
        #     ActionChains(driver).key_down(Keys.DOWN).perform()
        #     ActionChains(driver).key_down(Keys.DOWN).perform()
        # ActionChains(driver).move_by_offset(-960, -360).perform()
        time.sleep(1)
    time.sleep(2)
    driver.find_element_by_xpath(".//i[@class='el-icon el-icon-arrow-right']").click()
    time.sleep(2)
