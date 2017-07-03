from naive_bayes_child import NaiveBayes 
import json

#imagine body is title. I didn't want to fake more data
model = NaiveBayes("body","topic")

model.train('test_train.json')

#simulating the json we are dealing with. make a document constructor later
good_doc = {}
good_doc["body"] ="I love how much I love flowers"

goodExampleTopic = model.predict(good_doc)
print("Topic: " + goodExampleTopic)

#With X, I want to predict y where TOPIC is goodExampleTopic
modelSub = NaiveBayes("body","subtopic","topic",goodExampleTopic)
modelSub.train('test_train.json')

goodExampleSubtopic = modelSub.predict(good_doc)

print("subTopic: " + goodExampleSubtopic)

accuracy = model.test('test_train.json')

print("tested on training data: " + str(accuracy))