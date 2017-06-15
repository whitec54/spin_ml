from naive_bayes_child import NaiveBayes 
import json

model = NaiveBayes()

model.train('test_train.json')

#simulating the json we are dealing with. make a document constructor later
good_doc = {}
bad_doc = {}
bad_doc["body"] = "I hate how much I hate this shit"
good_doc["body"] ="I love how much I love that I am happy"

goodExamplePred = model.predict(good_doc)
badExamplePred = model.predict(bad_doc)

print("good: " + goodExamplePred)
print("bad: " + badExamplePred)

accuracy = model.test('test_train.json')

print("tested on training data: " + str(accuracy))