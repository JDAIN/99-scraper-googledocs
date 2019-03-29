import requests
import bs4
import re

enctab = dict()


def scrape_page(url='http://spys.one/en/socks-proxy-list/', soup='n'):
    """
    Scrape given link and create a beautiful soup object.
    - url:  Url to scrape.
    - soup: "n" to not create soup object and only return request response.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    data = {
        'xpp': '5',
        'xf1': '1'
    }

    request_url = requests.post(url, headers=headers, data=data)
    request_url.raise_for_status()
    # print(request_url.status_code)

    if request_url.status_code == 200:
        if soup == 'y':
            html_soup = bs4.BeautifulSoup(request_url.content, 'lxml')
            return html_soup
        return request_url


# Taken from https://github.com/xanderdin/scrape.spys.one.proxies :)
def fill_enctab(arg):
    """
    Fill enctab with values from the script
    with encoding values.
    @arg - script body
    """
    plain_values = [v for v in [x.split('=') for x in arg] if len(v[0]) == 4]
    for v in plain_values:
        enctab[v[0]] = int(v[1])
    other_values = [v for v in [x.split('=') for x in arg] if len(v[0]) == 6]
    for v in other_values:
        (a, b) = v[1].split('^')
        enctab[v[0]] = int(a) ^ enctab[b]


def calc_port(script):
    port = ''
    port_parts = re.findall('\+\(([a-z0-9^]+)\)+', script)
    for part in port_parts:
        (a, b) = part.split('^')
        port += str(enctab[a] ^ enctab[b])
    return port


def get_proxy_info(proxies_num=5):
    soup = scrape_page(soup='y')
    arg = soup.body.find(
        'script', attrs={'type': "text/javascript"}).text.split(';')
    fill_enctab(arg)  # Fills Encoding Tabs ^
    data = []
    proxy_info = {'ip': [], 'port': [], 'country': []}

    counter = 0

    for i, info in enumerate(soup.findAll('td', attrs={"colspan": "1"}), 1):
        info = info.find('font', class_='spy14')

        if info:

            if i % 3 == 0:
                proxy_info['ip'].append(data[0])
                proxy_info['country'].append(data[1])
                data = []
                counter += 1

            elif info.contents:
                if len(info.contents) == 2:
                    proxy_info['port'].append(
                        calc_port(str(info.contents[-1])))
                data.append(info.contents[0])
    return proxy_info


def scrape_and_get_only_proxies_list():
    """
    scraps and returns List with proxies in form [ip:port]
    """
    proxieslist = []
    proxies = get_proxy_info()
    for i in range(len(proxies['ip'])):
        proxieslist.append('{}:{}'.format(
            proxies['ip'][i], proxies['port'][i]))
        # print('IP: {}\nPORT: {}\nCOUNTRY: {}'.format(
        #     proxies['ip'][i], proxies['port'][i], proxies['country'][i]))
    print('Done scraping proxylist.')
    return proxieslist


def scrape_DACH_D_and_get_only_proxies_list():
    """
    scraps only DACH countrys + Denmark
    scraps and returns List with proxies in form [ip:port]
    """
    proxieslist = []
    # TODO filter countries out
    proxies = get_proxy_info()
    dach = ['Germany', 'Austria', 'Switzerland', 'Denmark']
    for i in range(len(proxies['ip'])):
        if proxies['country'][i] in dach:
            proxieslist.append('{}:{}'.format(
                proxies['ip'][i], proxies['port'][i]))
        # print('IP: {}\nPORT: {}\nCOUNTRY: {}'.format(
        #     proxies['ip'][i], proxies['port'][i], proxies['country'][i]))
    print('Done scraping proxylist.')
    return proxieslist


def scrape_DACH_close_countries_and_get_only_proxies_list():
    """
    scraps only DACH countrys + Denmark
    scraps and returns List with proxies in form [ip:port]
    """
    proxieslist = []
    # TODO filter countries out
    proxies = get_proxy_info()
    dach = ['Germany', 'Austria', 'Switzerland', 'Denmark', 'Poland', 'United Kingdom', 'Netherlands', 'Finland']
    for i in range(len(proxies['ip'])):
        if proxies['country'][i] in dach:
            proxieslist.append('{}:{}'.format(
                proxies['ip'][i], proxies['port'][i]))
        # print('IP: {}\nPORT: {}\nCOUNTRY: {}'.format(
        #     proxies['ip'][i], proxies['port'][i], proxies['country'][i]))
    print('Done scraping proxylist.')
    return proxieslist
