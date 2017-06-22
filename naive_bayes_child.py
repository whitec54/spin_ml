from model import Model 
import json


class NaiveBayes(Model):
	def __init__(self,X="body",y="topic",keepOnlyParam="",keepOnlyCond=""):
		self.trainedParameters = {}
		#{"label_name":|instances of that label| / |documents|}
		self.trainedParameters["labelProbs"] = {}	
		#{"label":{"word":prob}}
		self.trainedParameters["labelToWordBag"]={}
		self.X = X
		self.y = y
		self.keepOnlyParam = keepOnlyParam
		self.keepOnlyCond = keepOnlyCond

	#this is where all of the computation happen. Predict should do little to no work
	def train(self,file):
		trainData = self.load_data(file)		
		self.gen_label_prob(trainData)
		self.gen_label_to_wordbag(trainData)

	def test(self,file):
		data = self.load_data(file)

		correctCount = 0
		totalCount = len(data)
		for doc in data:
			
			prediction = self.predict(doc)
			correct = doc[self.y]
			if(correct == prediction):
				correctCount += 1

		return correctCount/totalCount

	def load_data(self,file):
		with open(file,'r') as trainFile:
			data = json.load(trainFile)

		if(self.keepOnlyParam != ""):
			data = [doc for doc in data if doc[self.keepOnlyParam] == self.keepOnlyCond]
	
		for doc in data:
			doc[self.X] = self.clean(doc[self.X])

		return data

	def gen_label_prob(self,trainData):
		docCount = len(trainData)
		labelCount = {}
		for doc in trainData:
			if(doc[self.y] in labelCount):
				labelCount[doc[self.y]] += 1
			else:
				labelCount[doc[self.y]] = 0

		for label, count in labelCount.items():
			self.trainedParameters["labelProbs"][label] = count/docCount


	def gen_label_to_wordbag(self,trainData):
		labelToWordBag = {}
		for doc in trainData:
			label = doc[self.y]

			if label not in labelToWordBag:
				labelToWordBag[label] = {}
				labelToWordBag[label]["totalWordCount"] = 1

			for word in doc[self.X]:
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
			labelGivenDoc = self.label_given_doc(label,labelProb,doc)
			if(labelGivenDoc > maxProb):
				maxProb = labelGivenDoc
				maxLabel = label

		return maxLabel

	def label_given_doc(self, label,labelProb,doc):
		wordProbProduct = 1
		for word in doc[self.X]:
			if word in self.trainedParameters["labelToWordBag"][label]:
				wordProb = self.trainedParameters["labelToWordBag"][label][word]/self.trainedParameters["labelToWordBag"][label]["totalWordCount"]
			else:
				wordProb = 1/self.trainedParameters["labelToWordBag"][label]["totalWordCount"]

			wordProbProduct *= wordProb

		if(wordProbProduct == 0): #hacky fix for reaalllyy small decimals going to 0, breaking product
			wordProbProduct = .001

		return labelProb * wordProbProduct

	def save_trained_data(self):
		outfileName = self.y +"_trainedOn_"+self.X+"NBayes.json"
		super().save_trained_data(outfileName)

	def load_trained_data(self,infileName):
		super().load_trained_data(infileName)

	def clean(self,text):
		return super().clean(text)