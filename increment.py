# nick fiacco and jack elder
# creates dictionary based on csv file for good / bad words

# add some usage documentation you bitch

from stock import *
import csv
from stock_analysis import *
from dictionarycreation import *
from tweet import Tweet
import datetime

companies = ["AAPL", "BRK.A", "CHL", "FB", "GE", "GOOG", "JNJ", "JPM", "MSFT", "NVS", "PG", "PTR", "WFC", "WMT", "XOM"]

def parse_csv(ticker):
    filename = 'tweet_data/' + str(ticker) + '.csv'

    tweet_list = []

    in_file = open(filename, 'r')
    reader = csv.reader(in_file, delimiter=',')

    for row in reader:
        tweet = Tweet(ticker, row[0], row[1], row[2], row[3])
        tweet_list.append(tweet)
    in_file.close()
    return tweet_list

def create_sentiment_dictionary():
    file = open("dict.txt", "r")
    sentiment_dictionary = {}
    for line in file:
            s = line.strip()
            sp = s.split(",")
            sentiment_dictionary[sp[0]] = int(sp[1])
    return sentiment_dictionary


def increment(ticker, interval):
    sentiment_dict = create_sentiment_dictionary()
    tweet_list = parse_csv(ticker)
    stock = Stock(ticker)
    for tweet in tweet_list:
        s = tweet.body.strip()
	
	# get the date of the tweet
	date = tweet.time
	tokens = date.split()
	if len(tokens) > 2:
 		dateStr = tokens[0] + " " + tokens[1] + " " + tokens[2] + " " + tokens[5]
		date_key = str(datetime.datetime.strptime(dateStr, '%a %b %d %Y').date())
	else:
		continue
       
	
	# determine the rate of change of the stock starting on date_key
	if date_key not in stock.prices:
		stock.prices[date_key] = getStockData(ticker, date, interval)
	
 
	# aggregate the tweet value based on our sentiment dictionary
	sp = s.split()
        for i in range(len(sp)):
            if sp[i] in sentiment_dict:
		if date_key in stock.values:
                	stock.values[date_key] += sentiment_dict[sp[i]]
		else:
			stock.values[date_key] = sentiment_dict[sp[i]]
	
    for key in stock.values:
	print str(stock) + " tweet value on " + key + " is " + str(stock.values[key]) + " and change is " + str(stock.prices[key])

    return stock


def regress(stock):

	value_list = []
	price_list = []

	for key in stock.values:
		if key in stock.prices:
			value_list.append(float(stock.values[key]))
			price_list.append(float(stock.prices[key]))
	
	yData = np.array(price_list).astype(np.float)
	xData = np.array(value_list).astype(np.float)
	m, c = np.polyfit(xData, yData, 1)
	print "Regression is :" + str(m)

def main():
    for stock in companies:
        scored_stock = increment(stock, 5)
	regress(scored_stock)

main()

