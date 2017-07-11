import numpy as np
import json
import string 
import re
from bad_words import badWords
from model import Model 
import math



class LogisticRegression(Model):
	def __init__(self,feature_name="body",label_name="topic",ngramLen=1):
		self.feature_name = feature_name
		self.label_name = label_name
		self.ngramLen = ngramLen

	def train(self,X,y,alpha=.0009,iters = 500000):
		m,n = X.shape
		init_theta = np.zeros((n,1))
		self.theta = self.descend(init_theta,X,y,alpha,iters)


	def test(self,X,y):
		m,n = X.shape
		preds = self.matrixPredict(X)
		bool_array = preds == y
		correctCount = np.sum(bool_array)

		return correctCount/m

	def learningCurve(self,X_train,y_train,X_cv,y_cv,alpha=.0009,iters = 500000):
		m,n = X_train.shape
		tenthIters = math.floor(iters/10);
		dummy_theta = np.zeros((n,1))

		trainCost = self.cost(X_train,y_train,dummy_theta)
		cvCost = self.cost(X_cv,y_cv,dummy_theta)

		print("Train Cost: "+str(trainCost))
		print("CV Cost: "+str(cvCost))
		print()

		for i in range(10):
			dummy_theta = self.descend(dummy_theta,X_train,y_train,alpha,tenthIters)
			trainCost = self.cost(X_train,y_train,dummy_theta)
			cvCost = self.cost(X_cv,y_cv,dummy_theta)

			print("Train Cost: "+str(trainCost))
			print("CV Cost: "+str(cvCost))
			print()

	def matrixPredict(self,X):
		theta = self.theta
		predsRaw = self.sigmoid(X.dot(theta))
		preds = np.round(predsRaw)

		return preds

	def docPredict(self,doc):
		text = doc[self.feature_name]
		n = len(self.feature_key_vector)
		textVector = np.zeros([1,n])

		ngrams = super().gen_ngrams(text.split(),self.ngramLen)

		for ngram in ngrams:
			if(ngram in (self.feature_key_vector)):
				ind = self.feature_key_vector.index(ngram)
				textVector[0][ind] += 1

		return self.matrixPredict(textVector)[0][0]

	def sigmoid(self,matrix):
		matrix = matrix * -1
		matrix = np.exp(matrix)
		matrix = np.add(matrix,1)
		matrix = np.power(matrix,-1)
		return matrix

	def next_theta(self,X,y,theta,alpha):
		m = len(y)

		preds = self.sigmoid(X.dot(theta))
		errors = np.subtract(preds,y)
		errors = np.transpose(errors)
		errorSums = errors.dot(X)
		errorSums = np.transpose(errorSums)
		gradient_step = ((alpha/m) * errorSums)
		nextTheta = np.subtract(theta,gradient_step)

		return nextTheta


	def cost(self,X,y,theta):
		m,n = X.shape
		preds = self.sigmoid(X.dot(theta));
		Err = ((-1 *y) * np.log(preds)) - ((1-y) * np.log(1-preds));

		J = np.sum(Err) / (m);
		return J

	def descend(self,init_theta,X,y,alpha,itters):
		temp_theta = init_theta
		for i in range(itters):
			temp_theta = self.next_theta(X,y,temp_theta,alpha)

		return temp_theta

	#add super call for save
	#add super call for load. (may need to change json to pickle. idk numpy arrays)

	def getMatrices(self,filename):
		return super().getMatrices(filename,self.ngramLen)



				

def testLogReg():
	classifier = LogisticRegression()
	X_train,X_cv,X_test,y_dict_train,y_dict_cv,y_dict_test = classifier.getMatrices("testdocs.json")

	y_train = y_dict_train["positive"]
	y_cv = y_dict_cv["positive"]
	y_test = y_dict_test["positive"]

	print(X_train)
	print()
	print(X_cv)
	print()
	print(X_test)
	print()
	print("***************************************")
	print()
	print(y_train)
	print()
	print(y_cv)
	print()
	print(y_test)
	print()
	print("***************************************")
	print()
	print(classifier.feature_key_vector)
	print(classifier.label_key_vector)

	classifier.train(X_train,y_train)
	accuracy = classifier.test(X_test,y_test)
	print(accuracy)
	print()
	
	dummy_doc = {
		"body":"love love love, it's great"
	}
	bool_prediction = classifier.docPredict(dummy_doc)

	print("dummy doc test:")
	print("For body: "+dummy_doc["body"])
	print("Trained on y_train['positive'] bool prediction is:")
	print(bool_prediction)

	classifier.learningCurve(X_train,y_train,X_cv,y_cv)

testLogReg()