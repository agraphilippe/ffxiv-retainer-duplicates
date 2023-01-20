import requests
import logging
from bs4 import BeautifulSoup
from collections import defaultdict
import configparser

# Read the config file
config = configparser.ConfigParser()
config.read('config.ini')
logging.basicConfig(format='%(message)s', level=logging.INFO)

# constants
CHARACTER_ID = config['DEFAULT']['CHARACTER_ID']
SESSION_COOKIE = config['DEFAULT']['SESSION_COOKIE']

session = requests.Session()
session.headers.update({'Cookie': SESSION_COOKIE})


def get_lodestone_data(url):
    try:
        with session.get(url) as response:
            response.raise_for_status()
            return response.text
    except requests.exceptions.RequestException as err:
        logging.error(
            "An error occured while trying to connect to the website. %s", err)
        raise SystemExit(err)

def extract_items(tag):
    return tag.div.div.div.div.div.div.find('div', class_="db-tooltip__item__txt").h2    


def process_html_data(html_data):
    try:
        soup = BeautifulSoup(html_data, features="html.parser")
        h2s = [extract_items(tag) for tag in soup.find_all('li', class_="item-list__list sys_item_row")]
        return [str(h2.string) if h2.span is None else str(h2.contents[0]) + '*' for h2 in h2s]
    except Exception as Argument:
        logging.exception(
            "An error occured while processing the html data, %s", Argument)
        return []


def download_and_parse_data(retainer_id):
    retainer_data = get_lodestone_data(f'https://fr.finalfantasyxiv.com/lodestone/character/{CHARACTER_ID}/retainer/{retainer_id}/baggage/')
    return process_html_data(retainer_data)


def fetch_retainers_ids():
    try:
        soup = BeautifulSoup(get_lodestone_data(
            f'https://fr.finalfantasyxiv.com/lodestone/character/{CHARACTER_ID}/retainer/'), features="html.parser")
        list = soup.find_all('div', class_="retainer__data")[0].ul
        return {li.string: parts[5] for li in list.find_all('li') for parts in [li.a['href'].split(('/'))]}
    except Exception as Argument:
        logging.exception(
            "An error occured while trying to connect to the website.")
        return {}


def print_duplicates(items):
    for name, retainers in items.items():
        if (len(retainers) > 1 or logging.root.level <= logging.DEBUG):
            logging.info(f'{name} :')
            for retainer in retainers:
                logging.info(f'  {retainer}')


def main():
    items = defaultdict(list)

    for retainer, id in fetch_retainers_ids().items():
        for name in download_and_parse_data(id):
            items[name].append(retainer)

    print_duplicates(items)


if __name__ == "__main__":
    main()
