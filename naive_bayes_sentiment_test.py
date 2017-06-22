from naive_bayes_child import NaiveBayes 
import json

model = NaiveBayes()

#model.train('Movie_Data/train/train.json')
model.load_trained_data("topic_trainedOn_body.json")
accuracy = model.test('Movie_Data/test/test.json')

print("accuracy: " + str(accuracy))

model.save_trained_data()
