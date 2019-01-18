# _*_ coding: utf-8 _*_
__author__ = 'LelandYan'
__date__ = '2018/9/24 13:01'

from concurrent.futures import ThreadPoolExecutor
import requests
from selenium import webdriver

# driver = webdriver.Chrome()
# driver.get('http://example.webscraping.com/places/default/search')
# driver.find_element_by_id('search_term').send_keys('a')
# js = "document.getElementById('page_size').options[1].text='1000'"
# driver.execute_script(js)
# driver.find_element_by_id('search').click()
# driver.implicitly_wait(30)
LOGIN_URL = 'http://example.webscraping.com/places/default/user/login'
LOGIN_EMAIL = 'example@webscraping.com'
LOGIN_PASSWORD = 'example'
driver = webdriver.Chrome()
driver.get(LOGIN_URL)
driver.find_element_by_id('auth_user_email').send_keys(LOGIN_EMAIL)
driver.find_element_by_id('auth_user_password').send_keys(LOGIN_PASSWORD)
driver.find_element_by_css_selector('td.w2p_fw input.btn').click()

# def task(url):
#     response = requests.get(url)
#     print(response)
#
#
# pool = ThreadPoolExecutor(7)
# url_list = [
#
# ]
# for url in url_list:
#     pool.submit(task, url)
# pool.shutdown()
