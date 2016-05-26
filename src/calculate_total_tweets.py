# Chris Davis
# Calculates total number of tweets gathered across all tickers

import csv

def get_num_tweets(ticker):
  filename = 'tweet_data/' + str(ticker) + '.csv'

  count = 0

  try:
    in_file = open(filename, 'rb')
    reader = csv.reader(in_file, delimiter=',')

    for row in reader:
      count +=1

    in_file.close()

  except Exception as e:
    print "No file found"

  finally:
    return count
    

ticker_list = ['AAPL', 'GOOG', 'MSFT', 'XOM', 'BRK.A', 'WFC', 'JNJ', 'GE', 'CHL', 'JPM','NVS', 'FB', 'WMT', 'PTR', 'PG']
total_tweets = 0

for ticker in ticker_list:
    total_tweets += get_num_tweets(ticker)

print total_tweets
