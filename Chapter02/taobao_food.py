# _*_ coding: utf-8 _*_
__author__ = 'LelandYan'
__date__ = '2019/1/23 19:54'

from selenium import webdriver

browser = webdriver.Chrome()

def search():
    browser.get("https://www.taobao.com")
