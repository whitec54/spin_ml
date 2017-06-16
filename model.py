import json

class Model:

	def __init__(self):
		self.trainedParameters = []

	#overload 'for doc in json.load(file): modifty trained params'
	def train(self,file,X,y):
		self.trainedParameters = "Define self.trained parameters with subModel -Model"

	#overload 'for doc in json.load(file): call predict and check'
	def test(self,file,X,y):
		successRate = 0
		print("success rate: " + str(successRate))

	#call on trained params only, very little computation
	def predict(self,document,X,y):
		return "label = overload this"


	def save_trained_data(self,outfileName):

		with open(outfileName, 'w') as outfile:
			json.dump(self.trainedParameters, outfile)

	def write_trained_data(self,infileName):
		with open(infileName,'r') as infile:
			self.trainedParameters = json.load(infile)