#!/bin/python

# Title: Stock Analysis
# Author: Nick Fiacco
# Date: 5/5/2016

# Code to parse date from Twitter based string
# Also fetches historical stock data using yahoo_finance api
# runs regression on historical share prices using numpy

from yahoo_finance import *
import datetime
import numpy as np

# date string format: Mon May 02 01:15:47 +0000 2016

tweetDate = "Mon May 02 01:15:47 +0000 2016"


# converts Twitter date string into python datetime object
def convertDate(tweetDate):

	tokens = tweetDate.split()
	dateStr = tokens[0] + " " + tokens[1] + " " + tokens[2] + " " + tokens[5]

	return datetime.datetime.strptime(dateStr, '%a %b %d %Y')



# given a list of stock prices, returns the rate of change using a linear regression
def getChangeRate(prices):

	npData = np.array(prices).astype(np.float)
	
	x = np.array(range(len(npData)))
 	m, c = np.polyfit(x, npData, 1)

	return m


# returns the rate of change as a percentage of the average price for the period
def getStockData(ticker, tweetDate, interval):

	tokens = tweetDate.split()
	if len(tokens) > 1:
		startDate = convertDate(tweetDate)
	else:
		startDate = datetime.datetime.strptime(tweetDate, '%Y-%m-%d')

	endDate = startDate + datetime.timedelta(days=interval)
#	print "Getting data for: " + ticker + " from " + str(startDate.date()) + " to " + str(endDate.date())

	stock = Share(ticker)

	results = stock.get_historical(str(startDate.date()), str(endDate.date()))

	prices = []
	price_sum = 0
	for result in results:
#		print result['Close']
		prices.append(float(result['Close']))
#		print "Price on " + result['Date'] + " at close was: " + result['Close']
		price_sum += float(result['Close'])

	if len(prices) > 1:
		changeRate = getChangeRate(prices)
		return (changeRate/price_sum)*1000
	else:
		return 0
#	print "Slope of regression fit to stock data: " + str(changeRate)


#getStockData('AAPL', tweetDate, 5)
getStockData('AAPL', "2016-05-17", 5)

