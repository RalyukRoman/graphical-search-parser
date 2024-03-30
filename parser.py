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
        with open('paths_for_parsing.json') as paths_for_parsing:
            self.parse_dict = json.load(paths_for_parsing)

    def get_headers(self) -> dict:
        with open('user_agent.json') as user_agent:
            templates = json.load(user_agent)
        return {
            'user-agent': random.choice(templates['user_agent'])
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
