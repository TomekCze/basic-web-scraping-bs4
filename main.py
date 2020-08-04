from bs4 import BeautifulSoup
from requests import get

URL = 'https://www.olx.pl/nieruchomosci/mieszkania/sprzedaz/pomorskie/'

page = get(URL)
bs = BeautifulSoup(page.content, 'html.parser')

for offer in bs.find_all('div', class_='offer-wrapper'):
    footer = offer.find('td', class_='bottom-cell')
    location = footer.find('small', class_='breadcrumb').get_text().strip().split(',')[0]
    title = offer.find('strong').get_text().strip()
    price = offer.find('p', class_='price').get_text().strip()

    print(location, title, price)
