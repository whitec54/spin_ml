from flask import Flask, jsonify, render_template, request, json
from main import BiasBot

app = Flask(__name__)

#default page
@app.route('/')
def index():
	return "Default page"

#Waiting for classification
#Need some data-stuff in the url probably
@app.route('/loading')
def loadingScreen():
	return "Loading screen"

#classification with articles
#Also need some data-stuff in the url
@app.route('/classification')
def classificationScreen():
	return "Classification screen"

if __name__ == "__main__":
	app.run(debug=True)
 