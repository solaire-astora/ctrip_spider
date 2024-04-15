import urllib.request
import urllib.error
from urllib.parse import quote
from bs4 import BeautifulSoup
import codecs
import re
import openpyxl


def ask_url(url):
    # 一般来说，只要有'user-agent'这一个信息就足够了，保险点可以加上cookie
    head = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36 Edg/98.0.1108.43'
    }
    request = urllib.request.Request(url=url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")

    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


pattern = r'sight.*suzhou11'
city_tag = 'suzhou11'


def parse_sight(html):
    soup = BeautifulSoup(html, "lxml")
    divs = soup.find_all('div', class_='list_mod2')
    for div in divs:
        div = div.find('div', class_='rdetailbox')
        address = div.find('dd', class_='ellipsis').text.strip()
        link_name = div.find('a', target='_blank').get('title')

        link = div.find('a', target='_blank').get('href')
        score_data = div.find('a', class_='score').find('strong')
        if score_data is not None:
            try:
                score = float(score_data.text)
            except (IndexError, ValueError):
                score = 0.0
        else:
            score = 0.0

        review_count_data = div.find('a', class_='recomment')
        if review_count_data is not None:
            try:
                review_count = re.findall(r'\d+', review_count_data.text)[0]
            except (IndexError, ValueError):
                review_count = 0
        else:
            review_count = 0

        match = re.search(pattern, link)
        if not match:
            continue
        return {
            'name': link_name,
            'address': address,
            'link': link,
            'score': score,
            'review_count': review_count
        }
    return None

def process_url(url):
    html = ask_url(url)
    data = parse_sight(html)
    return data

def to_unicode_escape(s):
    return codecs.unicode_escape_encode(s)[0].decode().replace('\\u', '%u')


with open('sights.txt', 'r', encoding='utf-8') as file:
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet['A1'] = 'Name'
    worksheet['B1'] = 'Address'
    worksheet['C1'] = 'Link'
    worksheet['D1'] = 'Score'
    worksheet['E1'] = 'Review Count'

    row = 2
    has_data = {}

    attractions = file.read().split(' ')
    for attr in attractions:
        unicode_name = to_unicode_escape(attr)
        target_url = 'https://you.ctrip.com/sight/' + city_tag + '.html?keywords=' + quote(unicode_name)
        data = process_url(target_url)

        if data is None:
            print(attr + ' not found')
            continue
        if data['name'] in has_data:
            print(attr + ' search to ' + data['name'] + ' already exist')
            continue
        has_data[data['name']] = data['name']
        print(attr + ' search to ' + str(data))
        for key, value in data.items():
            worksheet[f"{chr(ord('A') + list(data.keys()).index(key))}{row}"] = value
        row += 1
    workbook.save('output.xlsx')