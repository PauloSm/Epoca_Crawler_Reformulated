import requests
import collections
import re
import urlparse
import lxml.html
import csv


def download(url, user_agent='nice_guy', retrie=2):
    # type: (str, int) -> str
    header = {'user_agent': user_agent}
    try:
        r = requests.get(url, headers=header)
        r.raise_for_status()
        html = r.text
    except requests.HTTPError as e:
        html = None
        if retrie > 0 and r.status_code >= 500 < 600:
            print e
            return download(url, user_agent, retrie - 1)

    return html


def link_crawler(seed):
    seen = set()
    to_be_crawled = collections.deque()
    to_be_crawled.append(seed)
    while to_be_crawled:
        url = to_be_crawled.popleft()
        seen = url
        html = download(url)
        for lnk in get_links(html):
            if lnk.endwith('/p') and lnk not in seen:  # lnk[-2:] == '/p'
                get_info(lnk)
                link = urlparse.urljoin(seed, lnk)
                to_be_crawled.append(link)


def get_links(html):
    # pattern -> 'http://www.epocacosmeticos(.*?)/p' | '<a[^>]+href=["\'](.*?)["\']'
    pattern = re.compile('<a[^>]+href=["\'](.*?)["\']')
    return pattern.findall(html)


def get_info(html):
    tree = lxml.html.fromstring(html)
    product_name = tree.xpath(r"//section[@class='name_brand']/h1//text()")
    prduct_price = tree.xpath(r"//strong[@class='skuBestPrice']/text()")


def write_to_csv(infos):
    pass
    

# download('http://httpstat.us/500')
download('http://www.epocacosmeticos.com.br/')









