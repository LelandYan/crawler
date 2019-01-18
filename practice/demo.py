# _*_ coding: utf-8 _*_
__author__ = 'LelandYan'
__date__ = '2018/9/22 7:31'

import builtwith
import whois
from urllib import request
import re
from urllib.parse import *
import datetime
import time
import collections
from urllib.robotparser import *


# ID遍历爬虫
# import itertools
#
# max_error = 5
# num_error = 0
# for page in itertools.count(1):
#     url = 'http://example.webscraping.com/view/-%d' % page
#     html = download(url)
#     if html is None:
#         num_error += 1
#         if num_error == max_error:
#             break
#     else:
#         num_error = 0

# 链接爬虫
def download(url, headers=None, proxy=None, num_retries=None, data=None):
    print("Downloading: " + url)
    req = request.Request(url=url, headers=headers, data=data)
    opener = request.build_opener()
    if proxy:
        proxy_params = {urlparse(url=url).scheme: proxy}
        opener.add_handler(request.ProxyHandler(proxy_params))
    try:
        response = opener.open(req)
        html = response.read().decode('utf-8')
        code = response.code
    except request.URLError as e:
        print("Download error: " + e.reason)
        html = ""
        if hasattr(e, 'code'):
            code = e.code
            if num_retries > 0 and 500 <= code < 600:
                return download(url, headers, proxy, num_retries - 1, data)
        else:
            code = None
    return html


def link_crawler(seed_url, link_regex=None, delay=5, headers=None, max_depth=-1, max_url=10,
                 user_agent='wswp',
                 proxy=None,
                 num_retries=1):
    crawl_queue = collections.deque([seed_url])
    seen = {seed_url: 0}
    num_urls = 0
    rp = get_robots(seed_url)
    throttle = Throttle(delay)
    headers = headers or {}
    if user_agent:
        headers['User-agent'] = user_agent

    while crawl_queue:
        url = crawl_queue.pop()
        if rp.can_fetch(user_agent, url):
            throttle.wait(url)
            html = download(url, headers, proxy=proxy, num_retries=num_retries)
            links = []

            depth = seen[url]
            if depth != max_depth:
                if link_regex:
                    links.extend(urljoin(seed_url, link) for link in get_links(html) if re.search(link_regex, link))
                for link in links:
                    link = normalize(seed_url, link)
                    if link not in seen:
                        seen[link] = depth + 1
                        if same_domain(seed_url, link):
                            crawl_queue.append(link)
            num_urls += 1
            if num_urls == max_url:
                break
        else:
            print('Blocked by robots.txt', url)


def normalize(seed_url, link):
    link, _ = urldefrag(link)
    return urljoin(seed_url, link)


def same_domain(url, url2):
    return urlparse(url).netloc == urlparse(url2).netloc


def get_links(html):
    webpage_regex = re.compile(r'<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    return webpage_regex.findall(html)


def get_robots(url):
    rp = RobotFileParser()
    rp.set_url(urljoin(url, '/robots.txt'))
    rp.read()
    return rp


# 下载限度
class Throttle:
    """add a delay between downloads to the same domain
    """

    def __init__(self, delay):
        self.delay = delay
        self.domains = {}

    def wait(self, url):
        domain = urlparse(url).netloc
        last_accessed = self.domains.get(domain)

        if self.delay > 0 and last_accessed is not None:
            sleep_secs = self.delay - (datetime.datetime.now() - last_accessed).seconds
            if sleep_secs > 0:
                time.sleep(sleep_secs)
        self.domains[domain] = datetime.datetime.now()


if __name__ == '__main__':
    # link_crawler('http://example.webscraping.com', '/(index|view)',)
    # download('http://httpstat.us/500')
    # throttle = Throttle(5)
    # throttle.wait()
    # r1 = download('http://example.webscraping.com', '/(index|view)')
    # link_crawler(, delay=0, num_retries=1, user_agent='BadCrawler')
    # link_crawler('http://example.webscraping.com', '/(index|view)', delay=0, num_retries=1, user_agent='BadCrawler')
    link_crawler('http://example.webscraping.com/index', '/(index|view)', delay=0, num_retries=1, max_depth=-1,
                 user_agent='GoodCrawler')
    
