#in ML traditionaly: X = features; y = labels; theta = model parameters; J = cost function 

#todo:
	# O fix syntax everywhere. this is glorified pseudo code 
	# O test at all
	# O make descend itters smarter
	# X turn into a class

import numpy as np


class LogisticRegression:
	def __init__(self,X="body",y="topic",keepOnlyParam="",keepOnlyCond=""):
		self.X = X
		self.y = y
		self.keepOnlyParam = keepOnlyParam
		self.keepOnlyCond = keepOnlyCond

	def train(self,file,alpha=.01,itters = 300):
		self.X,self.y = self.load_data(file,X,y)
		self.theta = np.array() #make 0's len(X) later
		self.theta = self.descend(X,y,alpha,iters)


	def test(self,file,X,y)
		self.X,self.y = self.load_data(file,X,y)

		correctCount = 0
		totalCount = 0

		for(i in range(len(X))):
			example = X[i]
			pred = self.predict(example)
			if(pred == y[i]):
				correctCount += 1
			totalCount += 1

		return correctCount/totalCount

	def predict(self,doc):							#psuedo code. none of this words
		predSum = 0
		for(i in range(len(doc))):
			sum += doc[i] * self.theta[i]

		predRaw = sigmoid(predSum)

		return round(predRaw)				

	def load_data(self,file):
		with open(file,'r') as trainFile:
			data = json.load(trainFile)

		if(self.keepOnlyParam != ""):
			data = [doc for doc in data if doc[self.keepOnlyParam] == self.keepOnlyCond]
	
		for doc in data:
			doc[self.X] = self.clean(doc[self.X])

		for doc in data:
			#figure out all of the unique words and their counts
			#sort alpha so index defines word

		for doc in data:
			docArr = np.array() # 0s of correct len
			for word in bodyOrWhatEver:
				#lookup position in Master array
				#set that position in docArr to be true or count idk yet
				#append docArr to some master X, building matrix

			#just set y to be one or 0 MODIFY LATER TO DEAL WITH MULTIPLE OPTIONS

		return X, y

	def sigmoid(matrix):
		matrix = matrix * 1
		matrix = np.exp(matrix)
		matrix = np.add(matrix,1)
		matrix = matrix ** -1
		return matrix

	def next_gradient_step(self,X,y,theta,alpha):
		m = len(y)

		predictions = sigmoid(np.cross(X,theta))
		errors = preds - y
		errors = np.transpose(errors)
		errorSums = np.cross(errors,X)
		errorSums = np.transpose(errorSums)
		nextTheta = theta - ((alpha/m) * errorSums)

		return nextTheta


	def cost(self,X,y,theta):
		preds = sigmoid(np.cross(X,theta));
		Err = ((-1 *y) * np.log(preds)) - ((1-y) * np.log(1-preds));

		J = np.sum(Err) / (m);

		return J

	def descend(self,X,y,alpha,itters):
		curCost = cost(X,y,theta)
		theta = self.theta

		for i in range(itters):
			tempTheta = next_gradient_step(X,y,theta,alpha)

			if(cost(X,y,tempTheta) < cost(X,y,theta)):
				theta = tempTheta
			else:
				break

		return theta

	#add super call for save

	#add super call for load. (may need to change json to pickle. idk numpy arrays)

	def clean(self,text):
		return super().clean(text)



