## Brief

Last weekend I
read [an article](https://www.smh.com.au/politics/federal/australians-want-jobkeeper-overpayments-given-back-to-taxpayers-20210827-p58mff.html)
regarding companies profiting from [JobKeeper](https://treasury.gov.au/coronavirus/jobkeeper) - an Australian government
relief program aimed to support business who were significantly impacted by the COVID-19 pandemic. I was disappointed,
yet not surprised, to learn that there was no public information provided by the government detailing the amount that
individual companies received from tax-payers. However, I thought that publicly-listed companies on the ASX might
mention JobKeeper & other COVID-related government support payments in their annual reports, and so, this project looks
to automate scrapping this data.

- How much money was paid out to shareholders in the form of dividends while the company received government hand-outs?
- How many companies maintained or exceeded their yearly profits while receiving JobKeeper?

A lot more news-coverage has happened since I began this project and, in all honesty, journalists have reported, in
greater detail & context, the same findings that I naively have made here. Some highlights:

* Public-backlash has led a number of companies to return Jobkeeper
  payments. [[1]](https://www.abc.net.au/news/2021-07-14/jobkeeper-repaid-comes-from-public-companies/100288376) [[2]](https://au.news.yahoo.com/21-companies-promise-to-return-297-million-in-job-keeper-who-are-they-045103580.html)
* Calls for transparency over these Jobkeeper payments continues to be fought over in
  parliament. [[3]](https://www.sbs.com.au/news/why-the-government-is-facing-a-push-for-transparency-on-jobkeeper/65f92ac7-81cc-4255-9dbd-c5ed55e1b2fa)

## Review

You can read _some_ data from this script in [REPORT.md](REPORT.md)  
In short, there were four typical company-responses:

* Companies do not explicitly mention government support payments, or they were lumped together with other payments
  within the financials.  
* Companies state they did not receive government support payments, but do not explain why; e.g. eligibility.  
* Companies state they did receive government support payments, but are repaying them.  
* Companies state they did receive government support payments, a lot of them & would kindly like you to bugger off.  

## Concessions

1. The board of directors has a fiduciary duty to act in the best interest of the company & its shareholders. The
   government had the responsibility to manage & police the JobKeeper program.
2. These scripts do not provide a complete picture to each company's response to government support.

## Repo

This repo is not a package, but a collection of scripts. If you wish to use it, it is expected that you have an
intermediate understanding of Python. 

This repo does a few things:

1. Grabs list of top stocks from the ASX; i.e. ASX20, ASX100, etc.
2. Searches & downloads annual reports
3. Reads PDF reports for keywords such as JobKeeper, COVID, etc.
    - Saves an PDF copy with keywords highlighted
    - Saves cropped photos of highlighted keywords
4. Grabs company data from Yahoo Finance; i.e. gross profits, dividends, etc.

Note that due to the nature of web-scrapping, these scripts may cease to function if endpoints & APIs change. 
