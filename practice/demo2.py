# _*_ coding: utf-8 _*_
__author__ = 'LelandYan'
__date__ = '2018/9/22 14:55'

import builtwith
import whois
from urllib import request
import re
from urllib.parse import *
import datetime
import time
import collections
from urllib.robotparser import *
import csv
import lxml.html


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


def link_crawler(seed_url, link_regex=None, delay=5, headers=None, max_depth=-1, max_url=-1,
                 user_agent='Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
                 proxy=None,
                 num_retries=1, scrape_callback=None):
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
            if not re.search(r'(/?next=|//login?)', url):
                html = download(url, headers, proxy=proxy, num_retries=num_retries)
                links = []
                if scrape_callback:
                    links.extend(scrape_callback(url, html) or [])
                depth = seen[url]
                if depth != max_depth:
                    if link_regex:
                        links.extend(urljoin(seed_url, link) for link in get_links(html) if re.search(link_regex, link))
                    for link in links:
                        link = normalize(seed_url, link)
                        if link not in seen:
                            seen[link] = depth + 1
                            if same_domain(seed_url, link):
                                if not re.search(r'(/?next=|//login?)', link):
                                    crawl_queue.append(link)
                num_urls += 1
                if num_urls == max_url:
                    break
        else:
            print('Blocked by robots.txt', url)


class ScrapeCallback:
    def __init__(self):
        self.writer = csv.writer(open('countries.csv', 'w', newline=""))
        self.fields = ('area', 'population', 'iso', 'country', 'capital', 'continent', 'tld', 'currency_name', 'phone',
                       'postal_code_format',
                       'postal_code_regex', 'languages', 'neighbours')
        self.writer.writerow(self.fields)

    def __call__(self, url, html):
        if re.search(r'/view/', url):
            tree = lxml.html.fromstring(html)
            row = []
            for field in self.fields:
                try:
                    message = tree.cssselect('table > tr#places_{}__row > td.w2p_fw'.format(field))[
                        0].text_content()
                except Exception as e:
                    message = None
                row.append(message)
            if row[3] == None:
                return
            self.writer.writerow(row)


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
    link_crawler(seed_url='http://example.webscraping.com/', link_regex=r'/(index|view)', max_depth=-1,
                 scrape_callback=None )
