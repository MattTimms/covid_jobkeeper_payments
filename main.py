from src.asx_index_scrapper import get_index_companies
from src.asx_scrapper import download_annual_reports
import yfinance as yf
import datetime
import locale

top_20_companies = get_index_companies(20)


locale.setlocale(locale.LC_ALL, '')

for company in top_20_companies:
    download_annual_reports(*company)

    yf_ticker = yf.Ticker(f'{company.code}.AX')

    print(yf_ticker.financials.loc['Gross Profit', :])

    dividends = yf_ticker.dividends
    n_share_outstanding = yf_ticker.info['sharesOutstanding']
    dividends_cash = dividends[datetime.datetime(2018, 1, 1):] * n_share_outstanding
    print(dividends_cash.apply(lambda x: locale.currency(x, grouping=True)))



    print(1)