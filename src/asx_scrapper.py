import os
import re
from typing import Dict, List
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

DATA_DST = os.getenv('DATA_DST', default='./tmp/')

# Define endpoint & headers
endpoint = "https://www.asx.com.au/"
session = requests.session()
session.hooks = {
    'response': lambda r, *args, **kwargs: r.raise_for_status()
}


def get_announcements(company_code: str, year: int) -> Dict[str, str]:
    """ Returns dict of announcement name & respective pdf url for given stock code. """
    url = urljoin(endpoint, 'asx/v2/statistics/announcements.do')
    response = session.get(url=url,
                           params={
                               'by': 'asxCode',
                               'asxCode': company_code,
                               'timeframe': 'Y',
                               'year': str(year)
                           })

    # Parse & return announcements & their pdf urls
    soup = BeautifulSoup(response.text, 'html.parser')
    try:
        announcements_anchors = soup.find('announcement_data').find_all('a')
    except AttributeError:  # Usually because no documents exist
        return {}
    return {anchor_tag.contents[0].lstrip(): anchor_tag['href'] for anchor_tag in announcements_anchors}


def download_announcement(output_path: str, url_path: str):
    # Get true url from redirect
    url = urljoin(endpoint, url_path)
    response = session.get(url=url)
    soup = BeautifulSoup(response.text, 'html.parser')
    pdf_url_path = soup.find('input', {'name': 'pdfURL'})['value']

    # Download pdf
    url = urljoin(endpoint, pdf_url_path)
    response = session.get(url=url)
    with open(output_path, 'wb') as f:
        f.write(response.content)


_pattern_annual_report = re.compile('Annual Report', flags=re.IGNORECASE)
_pattern_agm = re.compile('Annual General Meeting', flags=re.IGNORECASE)


def download_annual_reports(code: str, name: str) -> List[str]:
    company_code = code.upper()

    announcements = {title: url for year in [2020, 2021] for title, url in get_announcements(code, year).items()}
    annual_report_ann = list(filter(lambda title: _pattern_annual_report.search(title), announcements.keys()))
    if not annual_report_ann:
        annual_report_ann = list(filter(lambda title: _pattern_agm.search(title), announcements.keys()))

    output_dir = os.path.join(DATA_DST, f'{company_code} - {name}')
    os.makedirs(output_dir, exist_ok=True)

    file_paths = []
    for title in annual_report_ann:
        output_file_path = os.path.join(output_dir, f'{title.replace("/", "-")}.pdf')
        if not os.path.exists(output_file_path):
            download_announcement(output_file_path, announcements[title])
        file_paths.append(output_file_path)
    return file_paths
