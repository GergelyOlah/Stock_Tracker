import requests
from bs4 import BeautifulSoup
import re
import datetime

#Ideas:
#-Stoploss
#-send email alert

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


def stock_query():
    """Interactice command line tool that retrieves price info of selected stocks."""

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
        return None

def tracker(stock_list):
    """Tracks the price of predefined stocks."""

    stock_data = list()

    for stock in stock_list:
        url = url_constructor(stock)
        price = prices(url)
        news = top_news(url)
        stock_data.append([price, news])

    with open("stock_database.txt", "w") as f:
        for entry in stock_data:
            f.write(str(entry))
            f.write("\n")


stock_list = ["^GSPC", "TSLA", "BRK-B", "BTC-USD", "ETH-USD", "VUTY.L", "0P0000TKZK.L", "0P0000TKZI.L", "0P0000TKZH.L"]
tracker(stock_list)

#if __name__ == "__main__":
#    stock_query()
