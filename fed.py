import requests
from bs4 import BeautifulSoup

url = 'https://www.federalreserve.gov/econres/feds/2025.htm'

page = requests.get(url)

soup = BeautifulSoup(page.text, 'html.parser')

results = soup.find_all('div', class_='col-xs-12 col-md-12 col-sm-12')
#print(results)

'''
for p in results:
    title = p.find_all('h5')
    title_records = [t.get_text() for t in title[2:]]
'''

for p in results:
    date = p.find_all('time')
    date_records = [t.get_text().strip() for t in date]


