# _*_ coding: utf-8 _*_
__author__ = 'LelandYan'
__date__ = '2018/9/23 8:51'

import lxml.html
from downloader import Download
import json
import string
import csv

FIELDS = ('area', 'population', 'iso', 'country', 'capital', 'continent', 'tld', 'currency_name', 'phone',
          'postal_code_format',
          'postal_code_regex', 'languages', 'neighbours')
writer = csv.writer(open('countries2.txt', 'w',newline=""))
writer.writerow(('country',))
D = Download()
html = D('http://example.webscraping.com/places/ajax/search.json?&search_term=.&page_size=1000&page=0')
ajax = json.loads(html)
for record in ajax['records']:
    row = record['country']
    writer.writerow((row,))
# url = 'http://example.webscraping.com/places/ajax/search.json?&search_term={}&page_size=20&page={}'
# countries = set()
# for letter in string.ascii_lowercase:
#     page = 0
#     while True:
#         html = D(url.format(letter, page))
#         try:
#             ajax = json.loads(html)
#         except ValueError as e:
#             print(e)
#             ajax = None
#         else:
#             for record in ajax['records']:
#                 countries.add(record['country'])
#         page += 1
#         if ajax is None or page >= ajax['num_pages']:
#             break
#     open('countries.txt', 'w').write('\n'.join(sorted(countries)))
# html = D(url)
# print(json.loads(html))
# tree = lxml.html.fromstring(html)
# results = tree.cssselect('div#result a')
# print(results)
