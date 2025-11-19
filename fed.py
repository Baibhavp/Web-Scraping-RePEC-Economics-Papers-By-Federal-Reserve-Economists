import requests
from bs4 import BeautifulSoup

url = 'https://www.federalreserve.gov/econres/feds/2025.htm'

page = requests.get(url)

soup = BeautifulSoup(page.text, 'html.parser')

results = soup.find_all('div', attrs={'class': 'row'})
print(results)

records = []
for result in results:
    title = result.find_all('div', class_='h5')
    print(title)
    #authors = result.find_all('div', class_='authors')




