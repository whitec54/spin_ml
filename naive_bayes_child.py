from model import Model 
import json

class NaiveBayes(Model):
	def __init__(self):
		self.trainedParameters = {}
		#{"label_name":|instances of that label| / |documents|}
		self.trainedParameters["labelProbs"] = {}	
		#{"label":{"word":prob}}
		self.trainedParameters["labelToWordBag"]={}

	#this is where all of the computation happen. Predict should do little to no word
	def train(self,file):
		with open(file,'r') as trainFile:
			self.trainData = json.load(trainFile)

		self.gen_label_prob()
		self.gen_label_to_wordbag()

		del(self.trainData)

	def test(self,file):
		with open(file,'r') as testFile:
			data = json.load(testFile)

		correctCount = 0
		totalCount = len(data)

		for doc in data:
			prediction = self.predict(doc)
			correct = doc["topic"]
			if(correct == prediction):
				correctCount += 1
			

		return correctCount/totalCount

	def gen_label_prob(self):
		docCount = len(self.trainData)
		labelCount = {}

		for doc in self.trainData:
			if(doc["topic"] in labelCount):
				labelCount[doc["topic"]] += 1
			else:
				labelCount[doc["topic"]] = 0

		for label, count in labelCount.items():
			self.trainedParameters["labelProbs"][label] = count/docCount


	def gen_label_to_wordbag(self):
		labelToWordBag = {}

		for doc in self.trainData:
			label = doc["topic"]
			if label not in labelToWordBag:
				labelToWordBag[label] = {}
				labelToWordBag[label]["totalWordCount"] = 1

			for word in doc["body"]:
				labelToWordBag[label]["totalWordCount"] += 1

				if word in labelToWordBag[label]:
					labelToWordBag[label][word] += 1
				else:
					labelToWordBag[label][word] = 1

		self.trainedParameters["labelToWordBag"] = labelToWordBag


	#note there is extremely little computation. we are just calling on self.trainedParameters
	def predict(self,doc):
		maxProb = 0
		maxLabel = ""

		for label,labelProb in self.trainedParameters["labelProbs"].items():
			wordProbProduct = 1

			#probably make this a function
			for word in doc["body"]:
				if word in self.trainedParameters["labelToWordBag"][label]:
					wordProb = self.trainedParameters["labelToWordBag"][label][word]/self.trainedParameters["labelToWordBag"][label]["totalWordCount"]
				else:
					wordProb = 1/self.trainedParameters["labelToWordBag"][label]["totalWordCount"]

				wordProbProduct *= wordProb

			labelGivenDocProb = labelProb * wordProbProduct


			if(labelGivenDocProb > maxProb):
				maxProb = labelGivenDocProb
				maxLabel = label

		return maxLabel

	def save_trained_data(self,infileName):
		super().save_usefull_data(self,infileName)

	def write_trained_data(self,outfileName):
		super().write_trained_data(self,outfileName)