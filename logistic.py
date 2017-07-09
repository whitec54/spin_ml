#in ML traditionaly: X = features; y = labels; theta = model parameters; J = cost function 

#todo:
	# O fix syntax everywhere. this is glorified pseudo code 
	# O test at all
	# O make descend itters smarter
	# X turn into a class

import numpy as np
import json
import string 
import re
from bad_words import badWords
from model import Model 



class LogisticRegression(Model):
	def __init__(self,filename,feature_name="body",label_name="topic",ngramLen = 1):
		self.feature_name = feature_name
		self.label_name = label_name

		self.X,self.y_dict = self.genTrainMatrix(filename,ngramLen)

		self.m,self.n = self.X.shape
		self.X = np.insert(self.X, 0, 1, axis=1) #add bais col of ones in front

		self.theta = np.zeros((self.n+1,1))


	def train(self,X,y,alpha=.0009,iters = 500000):
		self.theta = self.descend(X,y,alpha,iters)


	def test(self,X,y):
		preds = self.predict(X)
		bool_array = preds == y
		correctCount = np.sum(bool_array)

		return correctCount/self.m

	def predict(self,X):
		theta = self.theta
		predsRaw = self.sigmoid(X.dot(theta))
		preds = np.round(predsRaw)

		return preds

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
		preds = self.sigmoid(X.dot(theta));
		Err = ((-1 *y) * np.log(preds)) - ((1-y) * np.log(1-preds));

		J = np.sum(Err) / (m);
		return J

	def descend(self,X,y,alpha,itters):
		temp_theta = self.theta

		for i in range(itters):
			temp_theta = self.next_theta(X,y,temp_theta,alpha)

		return temp_theta

	#add super call for save
	#add super call for load. (may need to change json to pickle. idk numpy arrays)

	def clean(self,text):
		return super().clean(text)

	def genTrainMatrix(self,filename,ngramLen=1):
		return super().genTrainMatrix(filename,ngramLen)

	def getTrainMatrix(self):
		return self.X,self.y_dict

				

def testLogReg():
	classifier = LogisticRegression("testdocs.json")
	X,y_dict = classifier.getTrainMatrix()

	y = y_dict["positive"]

	classifier.train(X,y)
	accuracy = classifier.test(X,y)
	print(accuracy)

testLogReg()