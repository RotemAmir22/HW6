# *************** HOMEWORK 6 ***************
# TODO: GOOD LUCK!
import yfinance as yf
from datetime import date
from matplotlib import pyplot as plt


# ****************************************************** Start **********************************************


def get_object_single_stock(name_stock, start='1980-01-01', end=date.today(), interval='5d'):
    """
    gets a stock name and returns the following data as DataFrame in given time frame and interval:
    Open, High, Low, Close ,Volume, Dividends,Stock Splits
    :param name_stock: stock name
    :param start: start date of time frame
    :param end: end date of time frame
    :param interval: interval of data to display in time frame (e.g. time frame - 1 month, interval - 1 week ->
                     display: once for every week(interval) in month(time frame)
    :return: Data frame of data
    """
    stock = yf.Ticker(name_stock)
    stock_info = stock.history(interval, interval, start, end)
    return stock_info


def get_object_multiple_stock(list_stock, start='1980-01-01', end=date.today(), interval='5d'):
    """
    gets a list of stock names and returns data about stock in given time frame and interval
    data: Open, High, Low, Close ,Volume, Dividends,Stock Splits
    :param list_stock: list of stock names
    :param start: start date of time frame
    :param end: end date of time frame
    :param interval: interval of data to display in time frame (e.g. time frame - 1 month, interval - 1 week ->
                     display: once for every week(interval) in month(time frame)
    :return: dictionary of stocks and stock data: key = stock name, value = Data Frame
    """
    stock_dic = {}
    for stock in list_stock:
        stock_dic[stock] = get_object_single_stock(stock, start, end, interval)  # help from other function
    return stock_dic


def get_object_multiple_stock_v2(list_stock, start='1980-01-01', end=date.today(), interval='5d'):
    """
    for a list of stock names, returns data in given time frame and interval
    data: Open, High, Low, Close ,Volume, Dividends,Stock Splits
    :param list_stock: list of stock names
    :param start: start date of time frame
    :param end: end date of time frame
    :param interval: interval of data to display in time frame (e.g. time frame - 1 month, interval - 1 week ->
                     display: once for every week(interval) in month(time frame)
    :return: data frame of all the data
    """
    stocks = yf.download(list_stock, start, end, interval=interval, group_by='ticker')
    return stocks



# ******************************************************PART 1 - info**********************************************
def daily_return(stock):
    """
    gets a Data Frame of a specific stock and returns the average and std of percentage of daily return
    :param stock: Data Frame of stock
    :return: average and std of percentage of daily return
    """
    lst_of_percentage = []
    for index in range(1, len(stock['Close'])):
        percentage = ((stock["Close"][index] - stock["Close"][index - 1]) / stock["Close"][index - 1]) * 100
        lst_of_percentage.append(percentage)
    avg = float(sum(lst_of_percentage) / len(stock['Close']))
    std = sum((number - avg) ** 2 for number in lst_of_percentage) / len(lst_of_percentage)
    return avg, std ** 0.5


def information_of_stock(name_stock):
    """
    gets a stock name and return the dividend rate and website
    :param name_stock: stock name (str)
    :return: dividend rate and website
    """
    stock = yf.Ticker(name_stock)
    return stock.info['dividendRate'], stock.info['website']


# ******************************************************PART 2 - plot**********************************************
def plot_price(stock):
    """
    gets a Data Frame and creates a graph showing the growth of the close value per year.
    x axis -> year
    y axis -> close value
    :param stock: Date Frame of specific stock
    :return: AxesSubplot of graph
    """
    years = stock.index  # x axis
    close = stock['Close']  # y axis
    fig, ax = plt.subplots()
    ax.plot(years, close, 'mediumpurple')
    plt.xlabel('Date')  # x axis title
    plt.ylabel('Close value')  # y axis title
    plt.title('Stock Prices')
    plt.show()  # view graph
    return ax


# ******************************************************PART 3 - file**********************************************
def save_dividends(name_stock):
    """
    gets a stock name and creates a cvs file with the dividend values that are larger or equal the median of dividends
    :param name_stock: stock name
    """
    stock = yf.Ticker(name_stock)
    stock_div = stock.dividends
    median = stock.dividends.median()
    dic_for_doc = {}  # dictionary of info to write in file

    for index in range(len(stock_div)):
        if stock_div[index] >= median:
            dic_for_doc[stock.dividends.index[index]] = stock_div[index]  # update dict

    with open('Dividends.csv', 'w') as f:  # creates a new csv file
        f.write('Date,Dividends\n')
    with open('Dividends.csv', 'a') as f:  # updates csv file
        for key in dic_for_doc:
            f.write(str(key) + "," + str(dic_for_doc[key]) + "\n")
