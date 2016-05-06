
class Stock:
	def __init__(self, name, threshold = 5):
		self.name = name
		self.value = 0
		self.threshold = threshold

	def __str__(self):
		return str(self.name + " Score is " + str(self.value))

