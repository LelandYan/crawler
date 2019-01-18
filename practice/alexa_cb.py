# _*_ coding: utf-8 _*_
__author__ = 'LelandYan'
__date__ = '2018/9/23 17:32'

import csv
from zipfile import ZipFile
from downloader import Download
from io import StringIO
from link_crawler import link_crawler
from disk_cache import DiskCache


# D = Download()
# zipped_data = D('http://s3.amazonaws.com/alexa-static/top-1m.csv.zip')
# urls = []
# with ZipFile(StringIO(zipped_data)) as zf:
#     csv_filename = zf.namelist()[0]
#     print(csv_filename)
#     for _, website in csv.reader(zf.open(csv_filename)):
#         print(_ + "  " + website)
#         urls.append('http://' + website)


class AlexaCallback:
    def __init__(self, max_urls=100):
        self.max_urls = max_urls
        self.seed_url = 'http://s3.amazonaws.com/alexa-static/top-1m.csv.zip'

    def __call__(self, url, html):
        if url == self.seed_url:
            urls = []
            print(html)
            with ZipFile(StringIO(html)) as zf:
                csv_filename = zf.namelist()[0]
                for _, website in csv.reader(zf.open(csv_filename)):
                    urls.append('http://' + website)
                    if len(urls) == self.max_urls:
                        break
            return urls


if __name__ == '__main__':
    link_crawler(seed_url=AlexaCallback().seed_url, cache=DiskCache(), scrape_callback=AlexaCallback())
