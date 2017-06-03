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

class Document():
	def __init__(self):
		self.wordBag = {} #{word:num_instances}
		self.size = 0

	def get_word_count(self,word):
		res = 0
		if(word in self.word_counts):
			res = word_counts[word]


class BayesModel():
	def __init__(self, file):
		self.doc_count = 0
		self.word_count = 0
		self.label_to_count = {} #{label:num_instances}
		self.label_to_prior = {} #{label}
		self.label_to_docs {} # {label:[documents]}
		self.trained = False

		#TODO iterate over training file full of documents and set above
		#values accordingly 

	def get_label_prior(self,label):
		numer = 0
		denom = self.doc_count

		if label in label_to_count:
			numer = label_to_count[label]

		return float(numer)/float(denom)

	def word_given_label(self,word,label):
		total_words_in_label = 0
		total_word_matches = 0

		docs_with_label = []
		if label in self.label_to_to_doc:
			docs_with_label = self.label_to_docs[label]

		for doc in docs_with_label:
			total_word_matches += doc.get_word_count(word)
			total_words_in_label += doc.size

		return [float(total_word_matches)+1]/[float(total_words_in_label)+self.word_count]

	def label_given_document(self,label,doc):
		probabity_product = 1

		for word,count in doc:
			word_prob = [self.word_given_label(word,label)] ** count
			probabity_product *= word_prob

		return probabity_product

	def predict(self,doc):
		cur_max = float()
		max_label = "" 

		for label, count in self.label_to_count:
			prob = self.label_given_document(label,doc) * self.get_label_prior(label)
			if prob > cur_max:
				cur_max = prob
				max_label = label

		return label


		






		