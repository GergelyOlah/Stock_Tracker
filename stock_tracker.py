import requests
from bs4 import BeautifulSoup

#Ideas:
#-Stoploss
#-Daily change
#-Search stock
#-send email alert

def main():
    stock = str(input("""Which stock are you interested in? Type the ticker of the stock or choose from the most popular ones:
    -Tesla [TSLA]
    -Berkshire Hathaway [BRK-B]\n
    Ticker: """))

    url = url_constructor(stock)
    print("The current price of {} is {}.".format(stock, prices(url)[0]))
    print("It closed with a value of {}".format(prices(url)[1]))
    print("The daily change is %.")
    print("What is the stop loss value do you want to set up?")

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
        price_current = soup.find("span", {"class":"Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)"}).text + " USD"
        prices.append(price_current)

        price_prev_close = soup.find("td", {"data-test":"PREV_CLOSE-value"}).find("span").text + " USD"
        prices.append(price_prev_close)

    except:
        print("Website cannot be accessed. Please check if the stock exists and you typed the ticker correctly.")

    return prices


if __name__ == "__main__":
    main()
