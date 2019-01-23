# _*_ coding: utf-8 _*_
__author__ = 'LelandYan'
__date__ = '2019/1/23 7:36'

html = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title" name="dromouse"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1"><!-- Elsie --></a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>
<p class="story">...</p>
"""
from bs4 import BeautifulSoup
soup = BeautifulSoup(html, 'lxml')
print(soup.prettify())
print(soup.title.string)

# content/children 获取子节点
# descendants 获取子孙节点
# parent/parents 获取父子点和祖先节点

# find_all()


# css选择器 select() class 用点 id用# get_text()获取文本
