import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass
from typing import List

session = requests.session()
session.hooks = {
    'response': lambda r, *args, **kwargs: r.raise_for_status()
}
session.headers['User-agent'] = 'index-scrapper/1.0'

allowed_indexes = [
    20, 50, 100, 200, 300
]


@dataclass
class Company:
    code: str
    name: str


def get_index_companies(index: int = 20) -> List[Company]:
    if index not in allowed_indexes:
        raise ValueError(f'index must be in {allowed_indexes}')

    url = f"https://www.asx{index}list.com/"
    response = session.get(url=url)
    soup = BeautifulSoup(response.text, 'html.parser')

    companies = []
    for row in soup.find('tbody').children:
        if row == '\n':
            continue

        code, name = row.text[:3], row.text[3:]
        companies.append(Company(code, name))
    return companies
