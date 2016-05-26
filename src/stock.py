#!/usr/bin/env python

# jack elder and nick fiacco

class Stock:
	def __init__(self, name, threshold = 5):
		self.name = name

		# prices and values are dictionaries with key as date of tweet
		self.prices = {}
		self.values = {}
		self.words = {}
		self.threshold = threshold

	def __str__(self):
		return str(self.name)
