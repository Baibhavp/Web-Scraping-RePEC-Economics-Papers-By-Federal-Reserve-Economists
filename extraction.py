class ExtractInfo:

    def __init__(self, response):
        self.response = response

        dates = self.get_dates(response)
        fed_numbers = self.get_fed_numbers(response)
        titles = self.get_titles(response)
        authors = self.get_author_names(response)

        self.records = []

        for date, num, title, author in zip(dates, fed_numbers, titles, authors):
            self.records.append([date, num, title, author])


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