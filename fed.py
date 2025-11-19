import requests
from bs4 import BeautifulSoup
from extraction import ExtractInfo

url = 'https://www.federalreserve.gov/econres/feds/2025.htm'

page = requests.get(url)
# Ensures correct format of encoding for unique characters
# response.apparent_encoding scans the raw bytes (response.content) and tries to detect the most likely encoding.
page.encoding = page.apparent_encoding

soup = BeautifulSoup(page.text, 'html.parser')

results = soup.find_all('div', class_='col-xs-12 col-md-12 col-sm-12')

extract = ExtractInfo(results)

doi_links = extract.get_doi_link(results)


# Testing to extract jel codes
doi_url = doi_links[1]

r = requests.get(doi_url)
doi_page = BeautifulSoup(r.text, 'html.parser')

pdf_url = doi_page.find('a', string="Full Paper")['href']

full_pdf_link = "https://www.federalreserve.gov" + pdf_url
print(full_pdf_link)


