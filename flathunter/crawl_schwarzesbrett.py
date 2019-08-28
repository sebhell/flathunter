import logging
import time
import hashlib
import urllib.request

import requests
import re
from bs4 import BeautifulSoup, SoupStrainer

base_url = 'https://schwarzesbrett.bremen.de'

class CrawlSchwarzesBrettBremen:
    __log__ = logging.getLogger(__name__)
    URL_PATTERN = re.compile(r'https://schwarzesbrett\.bremen\.de')

    def __init__(self):
        logging.getLogger("requests").setLevel(logging.WARNING)

    def get_results(self, search_url):
        self.__log__.debug("Got search URL %s" % search_url)

        soup = self.get_page(search_url)

        # get data from first page
        entries = self.extract_data(soup)

        self.__log__.debug('Number of found entries: ' + str(len(entries)))

        return entries

    def get_page(self, search_url):
        cur_page = self.dump_html(search_url)
        return BeautifulSoup(cur_page, features='html.parser', parse_only=SoupStrainer(['ul', 'li']))

    def extract_data(self, soup):

        fetched_offers = []
        cur_date = time.strftime('%d.%m.%y')

        for ul_tag in soup.find_all('ul', {'class': 'content_list eintraege_list'}):
            print('ul_tag')
            for li_tag in ul_tag.find_all('li'):
                splitted_tag = li_tag.text.split()
                title = ' '.join(splitted_tag[:-1])
                date = splitted_tag[-1]
                if date == cur_date:
                    link = li_tag.find_all('a', href=True)[0]['href']
                    details = self.fetch_details(base_url + link)

                    details = {
                        'id': abs(hash(title)) % (10**8),
                        'url': base_url + link,
                        'title': title,
                        'price': 0,
                        'size': details,
                        'rooms': 0,
                        'address': base_url + link
                    }
                    fetched_offers.append(details)

        return fetched_offers


        self.__log__.debug('extracted: ' + str(entries))

        return entries

    def dump_html(self, url):
        with urllib.request.urlopen(url) as fp:
            html_page = fp.read()
            return html_page.decode('utf8')

    def fetch_details(self, url):
        soup = BeautifulSoup(self.dump_html(url), features='html.parser', parse_only=SoupStrainer('p'))
        return soup.find_all('p', {'class': 'entry_text'})[0].text

    def load_address(self, url):
        # # extract address from expose itself
        # exposeHTML = requests.get(url).content
        # exposeSoup = BeautifulSoup(exposeHTML, 'html.parser')
        # try:
        #     street_raw = exposeSoup.find(id="street-address").text
        # except AttributeError:
        #     street_raw=""
        # try:
        #     address_raw = exposeSoup.find(id="viewad-locality").text
        # except AttributeError:
        #     address_raw =""
        # address = address_raw.strip().replace("\n","") + " "+street_raw.strip()

        return ""
