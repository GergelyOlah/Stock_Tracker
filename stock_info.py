import requests
from bs4 import BeautifulSoup
import re

#Ideas:
#-Stoploss
#-send email alert

def main():
    """Retrieves price info of selected stocks."""

    stock = str(input("""Which stock are you interested in? Type the ticker of the stock or choose from the most popular ones:
    -Tesla [TSLA]
    -Berkshire Hathaway [BRK-B]
    -Bitcoin [BTC-USD]\n
    Ticker: """))
    url = url_constructor(stock)
    
    if prices(url) == None:
        return print("Website cannot be accessed. Please check if the stock exists and you typed the ticker correctly.") 

    price_current = prices(url)[0]
    price_prev_close = prices(url)[1]
    currency = prices(url)[2]
    daily_change = round(100*(float(price_current.replace(",",""))-float(price_prev_close.replace(",","")))/float(price_prev_close.replace(",","")), 2)
    
    print("The current price of {} is {} {}.".format(stock, price_current, currency))
    print("It closed with a value of {} {}".format(price_prev_close, currency))
    print("The daily change is {}%.".format(daily_change))

def url_constructor(stock):
    """Creates an URL for the required stock."""

    url = 'https://finance.yahoo.com/quote/{}?p={}&.tsrc=fin-srch'.format(stock, stock)
    return url


def prices(url):
    """Returns the current and the previous close price of a stock on the input website."""

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
        return prices

    except:
        return None


if __name__ == "__main__":
    main()
