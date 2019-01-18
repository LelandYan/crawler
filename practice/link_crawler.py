# _*_ coding: utf-8 _*_
__author__ = 'LelandYan'
__date__ = '2018/9/23 15:09'

import re
from urllib.parse import *
from urllib.robotparser import *
from downloader import Download


def link_crawler(seed_url, link_regex=None, delay=5, max_depth=-1, max_urls=-1, user_agent='Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36', proxies=None,
                 num_retries=1, scrape_callback=None, cache=None):
    crawl_queue = [seed_url]

    seen = {seed_url: 0}
    num_urls = 0
    rp = get_robots(seed_url)
    D = Download(delay=delay, user_agent=user_agent, proxies=proxies, num_retries=num_retries, cache=cache)

    while crawl_queue:
        url = crawl_queue.pop()
        depth = seen[url]

        if rp.can_fetch(user_agent, url):
            html = D(url)
            links = []
            if not re.search(r'(/?next=|//login?)', url):
                if scrape_callback:
                    links.extend(scrape_callback(url, html) or [])

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
                if num_urls == max_urls:
                    break
        else:
            print('Blocked by robots.txt', url)


def normalize(seed_url, link):
    # remove hash to avoid duplicates
    link, _ = urldefrag(link)
    return urljoin(seed_url, link)


def same_domain(url1, url2):
    return urlparse(url1).netloc == urlparse(url2).netloc


def get_robots(url):
    rp = RobotFileParser()
    rp.set_url(urljoin(url, '/robots.txt'))
    rp.read()
    return rp


def get_links(html):
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    return webpage_regex.findall(html)


