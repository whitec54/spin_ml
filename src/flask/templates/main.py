import config
import requests
import isodate
import math

class BiasBot:

	def __init__(self, x, y):
		self.x = x
		self.y = y
		#config stuff here

	def getSentiment(self):
		return "Here is some sentiment"

	def getClass(self):
		return "Here is some class"

	def getRelatedArticles(self):
		return"Here are some related articles"

if __name__ == "__main__":
	test = BiasBot()