# each day is an array, each element in the array is a different words
# first word in the dictionary will be the first word

# first we will need to create a dictionary containing every word that
# occurs in the entire data set

# then, for each day we initialize the value for every word to 0

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


def increment(ticker, interval):
	tweet_list = parse_csv(ticker)
	word_dict = {}
	word_dict_list = {}
	prices = {}

	# loop over every tweet in the data set
	for tweet in tweet_list:
		body = tweet.body.strip()
		words = body.split()
		for word in words:

			# add every word to the dictionary
			if word not in word_dict:
				word_dict[word] = 0

	# aggregate word frequencies on each day independently
	for tweet in tweet_list:

		# get the date of the tweet
		date = tweet.time
		tokens = date.split()
		if len(tokens) > 2:
			dateStr = tokens[0] + " " + tokens[1] + " " + tokens[2] + " " + tokens[5]
			date_key = str(datetime.datetime.strptime(dateStr, '%a %b %d %Y').date())
		else:
			continue

		# determine the rate of change of the stock starting on date_key
		if date_key not in prices:
			prices[date_key] = getStockData(ticker, date, interval)

		# examine each word in this tweet
		body = tweet.body.strip()
		words = body.split()
        for word in words:

			# create a new dictionary for this date
			if date_key not in word_dict_list:
				word_dict_list[date_key] = word_dict.copy()

			# increment the frequency of the word on this date
			word_dict_list[date_key][word] += 1.0


	# run the multivariate linear regression over stock price rate of change
	# with the variables being the various word frequencies on each day
	x_list = []
	y = []
	for key in word_dict_list:
		if key not in prices:
			continue

		y.append(prices[key])

		x = []
		for word in word_dict_list[key]:
			x.append(float(word_dict_list[key][word]))

		x_list.append(x)

	npX = np.array(x_list)
	npY = np.array(y)
	results = np.linalg.lstsq(npX, npY)

	return results[0]

def main():

    for stock in companies:
        coefficients = increment(stock, 5)
	print "Coefficients for " + str(stock) + " are "
	print coefficients

main()
