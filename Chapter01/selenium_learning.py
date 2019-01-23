# _*_ coding: utf-8 _*_
__author__ = 'LelandYan'
__date__ = '2019/1/23 8:00'


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# 声明浏览器对象
#browser = webdriver.Chrome()

# 访问页面
# browser = webdriver.Chrome()
# browser.get("https://www.taobao.com")
# print(browser.page_source)
# browser.close()

# 查找元素
# browser = webdriver.Chrome()
# browser.get("https://www.taobao.com")
# input_first = browser.find_element_by_css_selector("#q")
# print(input_first)

# 元素交互操作
import time
browser = webdriver.Chrome()
browser.get("https://www.taobao.com")
input = browser.find_element_by_id("q")
input.send_keys("iPhone")
time.sleep(1)
input.clear()
input.send_keys('iPad')
button = browser.find_elements_by_class_name("btn-search")[0]
button.click()