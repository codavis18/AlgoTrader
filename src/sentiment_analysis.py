#!/usr/bin/env python

# jack elder and nick fiacco
# creates dictionary based on csv file for good / bad words

# add some usage documentation you bitch

from stock import *
import csv
from stock_analysis import *
from tweet import Tweet
import datetime
import warnings
import matplotlib.pyplot as plot

companies = ["AAPL", "CHL", "FB", "GE", "GOOG", "JNJ", "JPM", "MSFT", "NVS", "PG", "PTR", "WFC", "WMT", "XOM"]

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


def increment(ticker, interval, sentiment_dict):
	tweet_list = parse_csv(ticker)
	stock = Stock(ticker)


	for tweet in tweet_list:
	        body = tweet.body.strip()

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
		words = body.split()
	        for word in words:

			# check if the word is in the dictionary
			if word in sentiment_dict:

				if date_key in stock.values:
		                	stock.values[date_key] += sentiment_dict[word]
				else:
					stock.values[date_key] = sentiment_dict[word]

				if date_key in stock.words:
					stock.words[date_key] += 1.0
				else:
					stock.words[date_key] = 10.0

	for key in stock.values:
		if key in stock.words:
			stock.values[key] = (stock.values[key] / stock.words[key]) *10

		print str(stock) + " tweet value on " + key + " is " + str(stock.values[key]) + " and change is " + str(stock.prices[key])

	return stock


def regress(stock):

	warnings.simplefilter('ignore', np.RankWarning)

	value_list = []
	price_list = []

	for key in stock.values:
		if key in stock.prices:
		#	print type(stock.prices[key])
		#	print type(stock.prices[key])
		#	if(type(stock.prices[key]) == int or type(stock.prices[key]) == 'numpy.float64'  and type(stock.values[key]) == int or type(stock.values[key]) == 'numpy.float64'):
			value_list.append(float(stock.values[key]))
			price_list.append(float(stock.prices[key]))

	if(len(value_list) > 1 and len(price_list) > 1 and len(value_list) == len(price_list)):
		yData = np.array(price_list).astype(np.float)
		xData = np.array(value_list).astype(np.float)

	#for value in value_list:
	#	print value

	#print "hello"

	#for price in price_list:
	#	print price

	results = np.polyfit(xData, yData, 1, full=True)
	coefficients = results[0]
	residuals = results[1]

	print "Regression is: " + str(coefficients[0]) + " with total residuals of " + str(residuals[0])

	return (xData, yData, coefficients)


def main():
    sentiment_dict = create_sentiment_dictionary()
    for stock in companies:
        scored_stock = increment(stock, 5, sentiment_dict)
	(x, y, c) = regress(scored_stock)

	fit_fn = np.poly1d(c)
	plot.plot(x, y, 'yo', x, fit_fn(x), '--k')
	plot.savefig("../plots/" + scored_stock.name + '.png')
	plot.close()
main()
