import requests
from bs4 import BeautifulSoup

url = 'https://www.federalreserve.gov/econres/feds/2025.htm'

page = requests.get(url)

soup = BeautifulSoup(page.text, 'html.parser')

results = soup.find_all('div', class_='col-xs-12 col-md-12 col-sm-12')
#print(results)


for p in results:
    titles = p.find_all('h5')
    records = [t.get_text() for t in titles[2:]]

print(records)

