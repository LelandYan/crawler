# _*_ coding: utf-8 _*_
__author__ = 'LelandYan'
__date__ = '2018/9/22 10:29'

import builtwith
import whois
from urllib import request
import re
from urllib.parse import *
from datetime import datetime
import time
import collections
from urllib.robotparser import *
from bs4 import BeautifulSoup
import lxml.html

FIELDS = ('area', 'population', 'iso', 'country', 'capital', 'continent', 'tld', 'currency_name', 'phone',
          'postal_code_format',
          'postal_code_regex', 'languages', 'neighbours')


def re_scraper(html):
    result = {}
    for fields in FIELDS:
        result[fields] = \
        re.search('<tr id="places_{}__row">.*?<td class="w2p_fw">(.*?)</td>'.format(fields), html).groups()[0]
        return result


def bs_scraper(html):
    soup = BeautifulSoup(html, 'html.parser')
    result = {}
    for fields in FIELDS:
        result[fields] = soup.find('table').find('tr', id='places_{}__row'.format(fields)).find('td',
                                                                                                class_='w2p_fw').text
    return result


def lxml_scraper(html):
    tree = lxml.html.fromstring(html)
    result = {}
    for fields in FIELDS:
        result[fields] = tree.cssselect('table > tr#places_{}__row > td.w2p_fw'.format(fields))[0].text_content()
    return result


def download(url, headers, proxy=None, num_retries=1, data=None):
    print('Downloading:', url)
    req = request.Request(url, data, headers)
    opener = request.build_opener()
    if proxy:
        proxy_params = {urlparse(url).scheme: proxy}
        opener.add_handler(request.ProxyHandler(proxy_params))
    try:
        response = opener.open(req)
        html = response.read().decode('utf-8')
        code = response.code
    except request.URLError as e:
        print('Download error:', e.reason)
        html = ''
        if hasattr(e, 'code'):
            code = e.code
            if num_retries > 0 and 500 <= code < 600:
                # retry 5XX HTTP errors
                return download(url, headers, proxy, num_retries - 1, data)
        else:
            code = None
    return html


def link_crawler(seed_url, link_regex=None, delay=5, max_depth=-1, max_urls=-1, headers=None, user_agent='wswp',
                 proxy=None, num_retries=1):
    """Crawl from the given seed URL following links matched by link_regex
    """
    # the queue of URL's that still need to be crawled
    crawl_queue = collections.deque([seed_url])
    # the URL's that have been seen and at what depth
    seen = {seed_url: 0}
    # track how many URL's have been downloaded
    num_urls = 0
    rp = get_robots(seed_url)
    throttle = Throttle(delay)
    headers = headers or {}
    if user_agent:
        headers['User-agent'] = user_agent

    while crawl_queue:
        url = crawl_queue.pop()
        # check url passes robots.txt restrictions
        if rp.can_fetch(user_agent, url):
            throttle.wait(url)
            html = download(url, headers, proxy=proxy, num_retries=num_retries)
            links = []

            depth = seen[url]
            if depth != max_depth:
                # can still crawl further
                if link_regex:
                    # filter for links matching our regular expression
                    links.extend(urljoin(seed_url, link) for link in get_links(html) if re.search(link_regex, link))

                for link in links:
                    link = normalize(seed_url, link)
                    # check whether already crawled this link
                    if link not in seen:
                        seen[link] = depth + 1
                        # check link is within same domain
                        if same_domain(seed_url, link):
                            # success! add this new link to queue
                            crawl_queue.append(link)

            # check whether have reached downloaded maximum
            num_urls += 1
            if num_urls == max_urls:
                break
        else:
            print('Blocked by robots.txt:', url)


class Throttle:
    """Throttle downloading by sleeping between requests to same domain
    """

    def __init__(self, delay):
        # amount of delay between downloads for each domain
        self.delay = delay
        # timestamp of when a domain was last accessed
        self.domains = {}

    def wait(self, url):
        domain = urlparse(url).netloc
        last_accessed = self.domains.get(domain)

        if self.delay > 0 and last_accessed is not None:
            sleep_secs = self.delay - (datetime.now() - last_accessed).seconds
            if sleep_secs > 0:
                time.sleep(sleep_secs)
        self.domains[domain] = datetime.now()


def normalize(seed_url, link):
    """Normalize this URL by removing hash and adding domain
    """
    link, _ = urldefrag(link)  # remove hash to avoid duplicates
    return urljoin(seed_url, link)


def same_domain(url1, url2):
    """Return True if both URL's belong to same domain
    """
    return urlparse(url1).netloc == urlparse(url2).netloc


def get_robots(url):
    """Initialize robots parser for this domain
    """
    rp = RobotFileParser()
    rp.set_url(urljoin(url, '/robots.txt'))
    rp.read()
    return rp


def get_links(html):
    """Return a list of links from html
    """
    # a regular expression to extract all links from the webpage
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    # list of all links from the webpage
    return webpage_regex.findall(html)


if __name__ == '__main__':
    # link_crawler('http://example.webscraping.com', '/(index|view)', delay=0, num_retries=1, user_agent='BadCrawler')
    # link_crawler('http://example.webscraping.com', '/(index|view)', delay=0, num_retries=1, max_depth=1,
    #              user_agent='GoodCrawler')
    NUM_ITERATIONS = 1000
    html = download('http://example.webscraping.com/places/default/view/Aland-Islands-2', {'Agent-user': 'wssp'})
    for name, scraper in [('Regular expressions', re_scraper), ('BeautifulSoup', bs_scraper), ('Lxml', lxml_scraper)]:
        start = time.time()
        for i in range(NUM_ITERATIONS):
            if scraper == re_scraper:
                re.purge()
            result = scraper(html)
        end = time.time()
        print(f'{name}:{end-start}')
