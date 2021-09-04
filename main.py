
import yfinance as yf
import datetime
import locale
import time
from pprint import pprint

from src.asx_index_scrapper import get_index_companies
from src.asx_scrapper import download_annual_reports
from src.pdf_reader import find_keyword

locale.setlocale(locale.LC_ALL, '')

keywords = ['JobKeeper', 'Covid']


def download_and_parse(code: str, name: str):
    file_paths = download_annual_reports(code, name)
    if not file_paths:
        print(f"!!! missing annual report for {code}")

    yf_ticker = yf.Ticker(f'{company.code}.AX')
    print(yf_ticker.financials.loc['Gross Profit', :])

    dividends = yf_ticker.dividends
    n_share_outstanding = yf_ticker.info['sharesOutstanding']
    dividends_cash = dividends[datetime.datetime(2018, 1, 1):] * n_share_outstanding
    print(dividends_cash.apply(lambda x: locale.currency(x, grouping=True)))

    for fp in file_paths:
        n_found = find_keyword(keywords, fp, save_crop_imgs=False, verbose=True)
        print(f"\n{fp}\n\tFound {n_found} instances of the keywords {keywords}")
        time.sleep(0.1)


if __name__ == '__main__':

    top_20_companies = get_index_companies(20)
    pprint(top_20_companies, indent=2)
    for company in top_20_companies:
        download_and_parse(code=company.code, name=company.name)

    # code = 'HVN'
    # yf_ticker = yf.Ticker(f'{code}.AX')
    # name = yf.Ticker(f'{code}.AX').info['longName']
    # download_and_parse(code=code, name=name)
    #
    # print(yf_ticker.financials.loc['Gross Profit', :].apply(lambda x: locale.currency(x, grouping=True)))
    # dividends = yf_ticker.dividends
    # n_share_outstanding = yf_ticker.info['sharesOutstanding']
    # dividends_cash = dividends[datetime.datetime(2018, 1, 1):] * n_share_outstanding
    # print(dividends_cash.apply(lambda x: locale.currency(x, grouping=True)))

    # keywords = ['JobKeeper']
    #
    # top_300_companies = get_index_companies(300)[37:]
    # for company in top_300_companies:
    #     download_and_parse(code=company.code, name=company.name)