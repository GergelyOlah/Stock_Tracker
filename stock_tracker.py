import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import csv
import os

def url_constructor(stock):
    """Creates an URL for the required stock to access the Yahooo Finance website."""

    url = 'https://finance.yahoo.com/quote/{}?p={}&.tsrc=fin-srch'.format(stock, stock)
    return url


def prices(url):
    """Returns price info of a stock from the input website.
    Format: [current price, previous close preice, currency, daily change]"""

    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')
    prices = []

    try:
        name = soup.find("div", {"id":"quote-header-info"}).find("h1", {"data-reactid":"7"}).text
        prices.append(name)

        price_current = soup.find("span", {"class":"Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)"}).text
        prices.append(price_current)

        price_prev_close = soup.find("td", {"data-test":"PREV_CLOSE-value"}).span.text
        prices.append(price_prev_close)

        currency_info = soup.find("div", {"id":"quote-header-info"}).find("div", {"data-reactid":"8"}).span.text
        currency = re.search(r"Currency in (.*)", currency_info)[1]
        prices.append(currency)

        daily_change = round(100*(float(price_current.replace(",",""))-float(price_prev_close.replace(",","")))/float(price_prev_close.replace(",","")), 2)
        prices.append(daily_change)

        return prices

    except:
        return None


def top_news(url):
    """Retrieves the latest news relevant to a particular stock. """
    
    response = requests.get(url)
    top_news = list()
    website = "https://finance.yahoo.com"

    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        news_block = soup.find_all("li", {"class": "js-stream-content Pos(r)"})
        summary = news_block[0].a.text
        link = website + news_block[0].a["href"]
        top_news.append(summary)
        top_news.append(link)
        return top_news
    except:
        return [None, None]


def stock_query():
    """Interactive command line tool that retrieves price info of selected stocks."""

    stock = str(input("""Which stock are you interested in? Type the ticker of the stock or choose from the most popular ones:
    -Tesla [TSLA]
    -Apple [AAPL]
    -Bitcoin [BTC-USD]\n
    Ticker: """))
    url = url_constructor(stock)
    price_info = prices(url)

    if price_info == None:
        return print("Website cannot be accessed. Please check if the stock exists and you typed the ticker correctly.") 

    price_current = price_info[1]
    price_prev_close = price_info[2]
    currency = price_info[3]
    daily_change = price_info[4]
    
    print("The current price of {} is {} {}.".format(stock, price_current, currency))
    print("It closed with a value of {} {}".format(price_prev_close, currency))
    print("The daily change is {}%.".format(daily_change))


def tracker(stock_list):
    """Tracks the price of predefined stocks."""

    date = datetime.now()
    date_string = date.strftime("%Y.%m.%d")

    with open("stock_database.csv", "w", newline="") as f_csv:
        
        csv_writer = csv.writer(f_csv)

        if os.stat("stock_database.csv").st_size == 0:
            header = ["Ticker", "Price", "Previous Close", "Currency", "Daily Change", "Date", "News headline", "News link"]
            csv_writer.writerow(header)

        for stock in stock_list:
            url = url_constructor(stock)
            stock_data = prices(url)
            news = top_news(url)
            stock_data.append(date_string)
            stock_data.append(news[0])
            stock_data.append(news[1])
            csv_writer.writerow(stock_data)

stock_list = ["^GSPC", "TSLA", "BRK-B", "BTC-USD", "ETH-USD", "VUTY.L", "0P0000TKZK.L", "0P0000TKZI.L", "0P0000TKZH.L"]
#stock_list = ["^GSPC", "TSLA"]
tracker(stock_list)

#if __name__ == "__main__":
   # stock_query()
