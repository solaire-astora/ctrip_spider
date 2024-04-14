import urllib.request
import urllib.error
from urllib.parse import quote
from bs4 import BeautifulSoup
import codecs

def to_unicode_escape(s):
    return codecs.unicode_escape_encode(s)[0].decode().replace('\\u', '%u')


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

def parse_sight(html):
    soup = BeautifulSoup(html, "lxml")



print(quote("鼓浪屿"))

//print(ask_url("https://you.ctrip.com/sight/Suzhou11.html?keywords=%u9F13%u6D6A%u5C7F"))
