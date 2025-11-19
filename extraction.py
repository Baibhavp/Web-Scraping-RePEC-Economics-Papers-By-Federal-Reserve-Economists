import requests
import re
from bs4 import BeautifulSoup
from io import BytesIO
from pdfminer.high_level import extract_text


class ExtractInfo:

    def __init__(self, response):
        self.response = response

        dates = self.get_dates(response)
        fed_numbers = self.get_fed_numbers(response)
        titles = self.get_titles(response)
        authors = self.get_author_names(response)
        jel_codes = self.get_jel_codes()

        self.records = [
            {
                "date" : date,
                "fed_number": num,
                "title": title,
                "authors": author,
                "jel_code": jel
            }
            for date,num,title,author,jel in zip(dates, fed_numbers, titles, authors, jel_codes)
        ]

    def get_titles(self, response):
        for p in response:
            title = p.find_all('h5')
            title_records = [t.get_text() for t in title[2:]]
        return title_records

    def get_author_names(self, response):
        for p in response:
            authors = p.find_all('div', class_='authors')
            authors_records = [t.get_text() for t in authors]
        return authors_records

    def get_dates(self, response):
        for p in response:
            date = p.find_all('time')
            date_records = [t.get_text().strip() for t in date]
        return date_records

    def get_fed_numbers(self, response):
        for p in response:
            feds_number = p.find_all('span', class_='badge badge--feds')
            feds_number_records = [t.get_text().strip() for t in feds_number]
        return feds_number_records

    def get_doi_link(self, response):
        for p in response:
            doi_tag = p.find_all('strong', string="DOI")
            doi_links = [doi.parent.get_text(strip=True).replace("DOI:", "").strip() for doi in doi_tag]
        return doi_links

    def get_jel_codes(self):
        doi_links = self.get_doi_link(self.response)
        jel_code_records = []

        for doi_url in doi_links:
            try:
                r = requests.get(doi_url)
                doi_page = BeautifulSoup(r.text, 'html.parser')
        
                pdf_url = doi_page.find('a', string="Full Paper")['href']
                full_pdf_link = "https://www.federalreserve.gov" + pdf_url
        
                # download the pdf into memory
                pdf_bytes = requests.get(full_pdf_link).content
        
                # wrap bytes in a file-like object
                pdf_file = BytesIO(pdf_bytes)
        
                # Extract text from pdf without saving the pdf in disk
                text = extract_text(pdf_file)
        
                # regex pattern , extract JEL codes
                jel_codes = re.findall(r"JEL Codes\s*[:–-]\s*([A-Z]\d{2}(?:,\s*[A-Z]\d{2})*)", text)
                jel_code_records.append(jel_codes)

            except TypeError:
                jel_code_records.append([])
                pass
