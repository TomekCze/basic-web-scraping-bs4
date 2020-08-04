from bs4 import BeautifulSoup
from requests import get
import sqlite3
from sys import argv


def parse_price(price):
    return float(price.replace(' ', '').replace('zł', '').replace(',', '.'))


def parse_page(number):
    print(f'Pracuję nad stroną {number}')
    page = get(f'{URL}&page={number}')
    bs = BeautifulSoup(page.content, 'html.parser')
    for offer in bs.find_all('div', class_='offer-wrapper'):
        footer = offer.find('td', class_='bottom-cell')
        location = footer.find('small', class_='breadcrumb').get_text().strip().split(',')[0]
        title = offer.find('strong').get_text().strip()
        price = parse_price(offer.find('p', class_='price').get_text().strip())
        # link = offer.find('a')

        cursor.execute('INSERT INTO offers VALUES (?, ?, ?)', (title, price, location))
        db.commit()


URL = 'https://www.olx.pl/nieruchomosci/mieszkania/sprzedaz/pomorskie/?search%5Bfilter_enum_rooms%5D%5B0%5D=one'
db = sqlite3.connect('dane.db')
cursor = db.cursor()
# python main.py setup
if len(argv) > 1 and argv[1] == 'setup':
    cursor.execute('''CREATE TABLE offers (name TEXT, price REAL, city TEXT)''')
    quit()

for page_number in range(1, 31):
    parse_page(page_number)

db.close()
