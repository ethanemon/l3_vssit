import collections
import logging
import csv

from bs4 import BeautifulSoup
import requests

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('shein')

ParseResult = collections.namedtuple(
    'ParseResult',
    (
        'link',
        'title',
        'img',
    ),
)

HEADERS = (
    'ссылка',
    'название',
    'картинка',
)

class Client:

    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/98.0.4758.102 Safari/537.36',
            'Accept-Language': 'ru',
        }
        self.result = []

    def load_page(self, page: int = None):
        url = 'https://ru.shein.com/Women-Skirts-c-1732.html?ici=ru_tab01navbar04menu03dir01&scici' \
              '=navbar_WomenHomePage~~tab01navbar04menu03dir01~~4_3_1~~real_1732~~~~0&srctype=category&userpath' \
              '=category%3E%D0%9E%D0%94%D0%95%D0%96%D0%94%D0%90%3E%D0%91%D0%A0%D0%AE%D0%9A%D0%98%20%D0%98%20%D0%AE%D0' \
              '%91%D0%9A%D0%98%3E%D0%AE%D0%B1%D0%BA%D0%B8 '
        res = self.session.get(url=url)
        res.raise_for_status()
        return res.text

    def parse_page(self, text: str):
        soup = BeautifulSoup(text, 'html.parser')

        container = soup.select('.S-product-item')

        for block in container:
            self.parse_block(block=block)

    def parse_block(self, block):
        a = block.select_one('.S-product-item__wrapper a')
        img_block = a.select_one('img')

        url = a['href']
        link = 'https://ru.shein.com/' + url
        img = 'https:' + img_block['src']
        name = a['aria-label']



        self.result.append(ParseResult(
            link=link,
            title=name,
            img=img,
        ))

        logger.debug('%s, %s, %s', link, name, img)
        logger.debug('=' * 100)

    def save_results(self):
        path = 'parser.csv'
        with open(path, 'w') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
            writer.writerow(HEADERS)
            for item in self.result:
                writer.writerow(item)

    def run(self):
        page = self.load_page()
        self.parse_page(page)
        self.save_results()

if __name__ == '__main__':
    client = Client()
    client.run()
