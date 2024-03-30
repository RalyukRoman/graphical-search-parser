# pip install requests parsel json random
import json
import requests
import random
from parsel import Selector, SelectorList
from requests import Response

class ScrapeParse():
    def __init__(self, url: str) -> None:
        self.url = "https://www.google.com/search?q=" + url
        self.headers = self.get_headers()
        self.response = self.make_request()
        self.selector = self.make_selector()
        self.parse_dict = {
            '':        {'title': 'div.yuRUbf div span a h3::text',
                         'link': 'div.yuRUbf div span a::attr(href)',
                         'name': 'div.GTRloc.CA5RN span::text',
                         'description': 'div.VwiC3b.yXK7lf.lVm3ye.r025kc.hJNv6b.Hdw6tb span',
                         'description_dop': 'div.VwiC3b.yXK7lf.lVm3ye.r025kc.hJNv6b.Hdw6tb::text'},
            '&tbm=vid': {'title': 'h3.LC20lb.MBeuO.DKV0Md::text',
                         'link': 'div.nhaZ2c div span a::attr(href)',
                         'name': 'div.gqF9jc span::text',
                         'description': 'div.fzUZNc div.ITZIwc::text'},
            '&tbm=nws': {'title': 'div.n0jPhd.ynAwRc.MBeuO.nDgy9d::text',
                         'link': 'a.WlydOe::attr(href)',
                         'name': 'div.MgUUmf.NUnG9d span::text',
                         'description': 'div.GI74Re.nDgy9d::text'},
            '&tbm=bks': {'title': 'div.bHexk.Tz5Hvf div span a h3.LC20lb.MBeuO.DKV0Md::text',
                         'link': 'div.bHexk.Tz5Hvf div span a::attr(href)',
                         'name': 'div.N96wpd a.fl span::text',
                         'description': 'div.cmlJmd span span::text',
                         'description_dop': 'div.cmlJmd.ETWPw span span'}
                    }

    def get_headers(self) -> dict:
        user_agent = [
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4899.78 Safari/537.36",
                        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/98.0.1108.62 Safari/537.36",
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4899.145 Safari/537.36",
                     ]
        return {
            'user-agent': user_agent[random.randint(0, 4)]
        }

    def make_request(self, url: str | None = None, headers: dict | None = None) -> Response:
        if url is None:
            url = self.url
        if headers is None:
            headers = self.headers
        return requests.get(url=url, headers=headers)

    def make_selector(self, response: Response | None = None) -> Selector:
        if response is None:
            response = self.response
        return Selector(text=response.text)

    def parse(self, data=None, bool_parse: bool = True, tab_dict_parse: str = '', page: int = 0) -> list[dict]:
        if data is None:
            data = []
        if bool_parse:
            self.selector = self.make_selector(response=self.make_request(url=self.url + tab_dict_parse + f'&start={page}'))
        if tab_dict_parse != '&tbm=nws':
            basis: SelectorList = self.selector.css('.dURPMd > div') if bool_parse else self.selector.css('.dURPMd div> div.ULSxyf')
        else:
            basis: SelectorList = self.selector.css('.dURPMd div.MjjYud div > div.SoaBEf')
        for part in basis:
            if part.css('div.ULSxyf').get() != None and bool_parse:
                continue
            title: str = part.css(self.parse_dict[tab_dict_parse]['title']).get()
            link: str = part.css(self.parse_dict[tab_dict_parse]['link']).get()
            name: str = part.css(self.parse_dict[tab_dict_parse]['name']).get()
            description: str = part.css(self.parse_dict[tab_dict_parse]['description']).get()
            if description in [None, '...', '... ', '... (', '... ( '] and tab_dict_parse in ['', '&tbm=bks']:
                description: str = part.css(self.parse_dict[tab_dict_parse]['description_dop']).get()
            if description != None:
                description = description.replace('/', '').replace('<span>', '').replace('<em>', '')
            if link == None:
                continue
            data.append({
                        'title': title,
                        'link': link,
                        'name': name,
                        'description': description
                        })
        if bool_parse and tab_dict_parse == '':
            return self.parse(data=data, bool_parse=False, tab_dict_parse=tab_dict_parse, page=page)
        else:
            return data

    def print(self, data: list[dict]) -> str:
        return json.dumps(data, indent=2, ensure_ascii=False)
