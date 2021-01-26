import requests
from bs4 import BeautifulSoup
import re

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


def main():
    """Retrieves price info of selected stocks."""

    stock = str(input("""Which stock are you interested in? Type the ticker of the stock or choose from the most popular ones:
    -Tesla [TSLA]
    -Berkshire Hathaway [BRK-B]
    -Bitcoin [BTC-USD]\n
    Ticker: """))
    url = url_constructor(stock)
    price_info = prices(url)

    if price_info == None:
        return print("Website cannot be accessed. Please check if the stock exists and you typed the ticker correctly.") 

    price_current = price_info[0]
    price_prev_close = price_info[1]
    currency = price_info[2]
    daily_change = price_info[3]
    
    print("The current price of {} is {} {}.".format(stock, price_current, currency))
    print("It closed with a value of {} {}".format(price_prev_close, currency))
    print("The daily change is {}%.".format(daily_change))

def tracker(stock_list):
    """Tracks he price of predefined stocks."""

    stock_data = dict()

    for stock in stock_list:
        url = url_constructor(stock)
        price = prices(url)
        stock_data[stock] = price

    with open("stock_database.txt", "w") as f:
        f.write(str(stock_data))

if __name__ == "__main__":
    main()
