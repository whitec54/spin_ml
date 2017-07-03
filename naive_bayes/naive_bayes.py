# Naive Bayes. More the former than the latter
#
# Test driven development means you drive towards testing it someday eventually right???
#
# based off the following lectures:
# https://www.youtube.com/watch?v=TpjPzKODuXo
# https://www.youtube.com/watch?v=0hxaqDbdIeE&t=196s
#
# ToDo: 
# finish init to actually read data
# Test something, anything at all 

import json

class Document():
	def __init__(self,line):
		self.wordBag = {} #{word:num_instances}
		self.size = 0
		line = line.split()

		for word in line:
			if word in self.wordBag:
				self.wordBag[word] += 1
			else:
				self.wordBag[word] = 1

			self.size+=1

	def get_word_count(self,word):
		res = 0
		if(word in self.wordBag):
			res = self.wordBag[word]

		return res

class BayesModel():
	def __init__(self, arr):
		self.doc_count = len(arr)
		self.word_count = 0
		self.label_to_count = {} #{label:num_instances}
		self.label_to_docs = {} # {label:[documents]}

		for obj in arr:
			label = obj["topic"]
			doc = Document(obj["body"])
			self.word_count += doc.size
			self.count_label(label)
			self.add_doc(label,doc)


	def count_label(self,label):
		if(label in self.label_to_count):
			self.label_to_count[label]+=1
		else:
			self.label_to_count[label] = 1

	def add_doc(self,label,doc):
		if label in self.label_to_docs:
			self.label_to_docs[label].append(doc)
		else:
			self.label_to_docs[label] = [doc]

	def get_label_prior(self,label):
		numer = 0
		denom = self.doc_count

		if label in self.label_to_count:
			numer = self.label_to_count[label]

		return float(numer)/float(denom)

	def word_given_label(self,word,label):
		total_words_in_label = 0
		total_word_matches = 0

		docs_with_label = []
		if label in self.label_to_docs:
			docs_with_label = self.label_to_docs[label]

		for doc in docs_with_label:
			total_word_matches += doc.get_word_count(word)
			total_words_in_label += doc.size

		return (float(total_word_matches))/(float(total_words_in_label))

	def label_given_document(self,label,doc):
		probabity_product = 1

		for word,count in doc.wordBag.items():
			word_prob = self.word_given_label(word,label) ** count

			#get rid of 0's to not break product with one word 
			if word_prob == 0:
				word_prob = 1/self.word_count

			probabity_product *= word_prob

		probabity_product *= self.get_label_prior(label)

		return probabity_product

	def predict(self,doc):
		cur_max = float()
		max_label = "" 

		for label, count in self.label_to_count.items():
			prob = self.label_given_document(label,doc)
			if prob > cur_max:
				cur_max = prob
				max_label = label

		return max_label

with open('test_train.json') as data_file:    
    data = json.load(data_file)

model = BayesModel(data)


doc1 = Document("hate shit sue")
doc2 = Document("love happy bob")

print(model.predict(doc1))
print(model.predict(doc2))