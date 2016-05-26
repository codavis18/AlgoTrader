#!/usr/bin/env python

# jack elder and nick fiacco
# used to store tweet data

class Tweet:
      # initializes variables
      def __init__(self, ticker, id, body, screen_name, time):
          self.ticker = ticker
          self.id = id
          self.time = time
          self.body = body
          self.username = screen_name
          self.value = 0

      # returns name, population, latitude and longitude when print called upon City class
      def __str__(self):
          return str(self.name) + "," + str(self.population) + "," + str(self.latitude) + "," + str(self.longitude)
