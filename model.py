import json
import string
from bad_words import badWords
import re
import numpy as np
import math

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

	def load_trained_data(self,infileName):
		with open(infileName,'r') as infile:
			self.trainedParameters = json.load(infile)


	def clean(self,text):
		toRemove = badWords()

		cleaned = ' '.join(word.strip(string.punctuation).lower() for word in text.split())#puntcuation, capitals
		cleaned = re.sub('<.*?>', ' ', cleaned) #html

		scripts = re.compile(r'<script[\s\S]+?/script>')
		cleaned = re.sub(scripts, "", cleaned)

		style = re.compile(r'<style[\s\S]+?/style>')
		cleaned = re.sub(style, "", cleaned)

		cleaned = cleaned.split()
		cleaned = [word for word in cleaned if word not in toRemove.words] # useless words

		return cleaned


	def gen_ngrams(self,words,ngramLen):
		ngrams=[]

		for i in range(len(words)):
			ngram = ""
			if(ngramLen>1 and (i-(ngramLen-1)) >=0 ):
				for j in range(i-(ngramLen-1),i+1):
					ngram += words[j]
			elif(ngramLen == 1):
				ngram = words[i]

			if(ngram != ""):
				ngrams.append(ngram)

		return ngrams


	def gen_ngram_to_count(self,data,feature_name,ngramLen):
		ngram_to_count = {}
		for doc in data:
			words = self.clean(doc[feature_name])
			ngrams = self.gen_ngrams(words,ngramLen)
			
			for ngram in ngrams:
				if ngram in ngram_to_count:
					ngram_to_count[ngram] += 1
				elif(ngram):
					ngram_to_count[ngram] = 1

		return ngram_to_count


	def get_unique_labels(self, data):
		labels = set()
		label_name = self.label_name

		for doc in data:
			labels.add(doc[label_name])

		return labels


	def gen_ngram_key_vector(self, data,ngramLen=1,remove_count = 0):
		ngram_count_list = []
		key_vector = []

		feature_name = self.feature_name
		label_name = self.label_name

		
		ngram_to_count = self.gen_ngram_to_count(data,feature_name,ngramLen)
		labels = self.get_unique_labels(data)

		#convert to array of tuples
		for key, value in ngram_to_count.items():
			temp = (key,value)
			ngram_count_list.append(temp)

		#sort it by count
		ngram_count_list = sorted(ngram_count_list, key=lambda x: x[1],reverse=True)

		#get just the words
		[key_vector.append(pair[0]) for pair in ngram_count_list]

		#chop down to size, keeping old len for printing
		og_len = len(key_vector)
		cap = len(key_vector)-remove_count
		key_vector = key_vector[0:cap]

		print("generated "+str(og_len)+" "+str(ngramLen)+"-grams")
		print("And kept the most common " + str(og_len-remove_count))

		return key_vector,labels

	def genWholeMatrices(self,filename,ngramLen=1):
		with open(filename,'r') as infile:
			data = json.load(infile)

		key_vector,labels = self.gen_ngram_key_vector(data,ngramLen)

		feature_name = self.feature_name
		label_name = self.label_name

		m = len(data)
		n = len(key_vector)
		X = np.zeros([m,n])

		y_dict = {}
		for label in labels:
			y_dict[label] = np.zeros([m,1])

		for k,doc in enumerate(data):
			row = np.zeros(n)
			words = self.clean(doc[feature_name])
			ngrams = self.gen_ngrams(words,ngramLen)
			for ngram in ngrams:
				if(ngram in (key_vector)):
					ind = key_vector.index(ngram)
					row[ind] += 1

			X[k] = row
			cur_label = doc[label_name]
			y_dict[cur_label][k][0] = 1

		self.label_key_vector = list(labels)
		self.feature_key_vector = key_vector
		return X,y_dict


	def shuffleUnison(self,X,y_dict):
		permutation = np.random.permutation(len(X))

		X = X[permutation]

		for label,bool_array in y_dict.items():
			y_dict[label] = bool_array[permutation]

		return X,y_dict

	def splitX(self,X_whole,m):
		trainEndInd = math.floor(m*0.6)
		cvEndInd = math.floor(m*0.8)

		X_train = X_whole[:trainEndInd,:]
		X_cv = X_whole[trainEndInd:cvEndInd,:]
		X_test = X_whole[cvEndInd:,:]

		return X_train,X_cv,X_test

	def splitYDict(self,y_dict_whole,m):
		trainEndInd = math.floor(m*0.6)
		cvEndInd = math.floor(m*0.8)

		y_dict_train = {}
		y_dict_cv = {}
		y_dict_test = {}

		for label,bool_array in y_dict_whole.items():
			y_dict_train[label] = bool_array[:trainEndInd,:]
			y_dict_cv[label] = bool_array[trainEndInd:cvEndInd,:]
			y_dict_test[label] = bool_array[cvEndInd:,:]

		return y_dict_train,y_dict_cv,y_dict_test

	def getMatrices(self,filename,ngramLen=1):
		X_whole,y_dict_whole = self.genWholeMatrices(filename,ngramLen)
		
		X_whole,y_dict_whole = self.shuffleUnison(X_whole,y_dict_whole)

		m,n = X_whole.shape
		X_train,X_cv,X_test = self.splitX(X_whole,m)
		y_dict_train,y_dict_cv,y_dict_test = self.splitYDict(y_dict_whole,m)

		return X_train,X_cv,X_test,y_dict_train,y_dict_cv,y_dict_test