#!/usr/bin/python2.7

# Basic classifiction functionality with Naive Bayes. File provided for the assignment on classification (IR course 2016/17)

import nltk.classify
import collections
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem.porter import *
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from featx import bag_of_non_stopwords, bag_of_words, high_information_words
from classification import precision_recall

from random import shuffle
from os import listdir # to read files
from os.path import isfile, join # to read files
import sys
import string

# return all the filenames in a folder
def get_filenames_in_folder(folder):
	return [f for f in listdir(folder) if isfile(join(folder, f))]

# reads all the files that correspond to the input list of categories and puts their contents in bags of words
def read_files(categories):
        #st = LancasterStemmer()
        #stemmer = PorterStemmer()
	feats = list ()
	print("\n##### Reading files...")
	for category in categories:
		files = get_filenames_in_folder('Volkskrant/' + category)
		num_files=0
		for f in files:
			data = open('Volkskrant/' + category + '/' + f, 'r').read().decode("utf-8")
			tokens = word_tokenize(data)
			#tokens = [token.lower() for token in tokens]   #nog geen verbetering gezien in accuracy
			for token in tokens:
                                for ch in token:
                                        if ch in string.punctuation:
                                                token = token.replace(ch,'')
                        #tokens = [st.stem(token) for token in tokens]
                        #tokens = [stemmer.stem(token) for token in tokens]
			#bag = bag_of_non_stopwords(tokens,stoplist='english')
                        bag = bag_of_words(tokens)
			feats.append((bag, category))
			#print len(tokens)
			num_files+=1
#			if num_files>=50: # you may want to de-comment this and the next line if you're doing tests (it just loads N documents instead of the whole collection so it runs faster
#				break
		
		print ("  Category %s, %i files read" % (category, num_files))

	return feats



# splits a labelled dataset into two disjoint subsets train and test
def split_train_test(feats, split=0.9):
	train_feats = []
	test_feats = []

	shuffle(feats) # randomise dataset before splitting into train and test
	cutoff = int(len(feats) * split)
	train_feats, test_feats = feats[:cutoff], feats[cutoff:]	

	print("\n##### Splitting datasets...")
	print("  Training set: %i" % len(train_feats))
	print("  Test set: %i" % len(test_feats))
	return train_feats, test_feats

# trains a classifier
def train(train_feats):
	#nb_classifier = NaiveBayesClassifier.train(train_feats)
	classifier = nltk.classify.NaiveBayesClassifier.train(train_feats)
	return classifier
	# the following code uses the classifier with add-1 smoothing (Laplace)
	# You may choose to use that instead
	#from nltk.probability import LaplaceProbDist
	#classifier = nltk.classify.NaiveBayesClassifier.train(train_feats, estimator=LaplaceProbDist)
	#return classifier

def calculate_f(precisions, recalls):
        f_measures = {}
        for categoryP in precisions:
                for categoryR in recalls:
                        if categoryP == categoryR:
                                f_ms = (2*precisions[categoryP]*recalls[categoryR])/(precisions[categoryP]+recalls[categoryR])
                                f_measures[categoryP] = f_ms
        return f_measures	

# prints accuracy, precision and recall
def evaluation(classifier, test_feats, categories):
	print ("\n##### Evaluation...")
	print("  Accuracy: %f" % nltk.classify.accuracy(classifier, test_feats))
	precisions, recalls = precision_recall(classifier, test_feats)
	f_measures = calculate_f(precisions, recalls)  

	print(" |-----------|-----------|-----------|-----------|")
	print(" |%-11s|%-11s|%-11s|%-11s|" % ("category","precision","recall","F-measure"))
	print(" |-----------|-----------|-----------|-----------|")
	for category in categories:
		print(" |%-11s|%-11f|%-11f|%-11s|" % (category, precisions[category], recalls[category], f_measures[category]))
	print(" |-----------|-----------|-----------|-----------|")
	return nltk.classify.accuracy(classifier, test_feats)


# show informative features
def analysis(classifier):
	print("\n##### Analysis...")
	classifier.show_most_informative_features(10)


# obtain the high information words
def high_information(feats, categories):
	print("\n##### Obtaining high information words...")

	labelled_words = [(category, []) for category in categories]

	#1. convert the formatting of our features to that required by high_information_words
	from collections import defaultdict
	words = defaultdict(list)
	all_words = list()
	for category in categories:
		words[category] = list()

	for feat in feats:
		category = feat[1]
		bag = feat[0]
		for w in bag.keys():
			words[category].append(w)
			all_words.append(w)
#		break

	labelled_words = [(category, words[category]) for category in categories]
	#print labelled_words

	#2. calculate high information words
	high_info_words = set(high_information_words(labelled_words))
	#print(high_info_words)
	#high_info_words contains a list of high-information words. You may want to use only these for classification.
	# You can restrict the words in a bag of words to be in a given 2nd list (e.g. in function read_files)
	# e.g. bag_of_words_in_set(words, high_info_words)

	print("  Number of words in the data: %i" % len(all_words))
	print("  Number of distinct words in the data: %i" % len(set(all_words)))
	print("  Number of distinct 'high-information' words in the data: %i" % len(high_info_words))

	return high_info_words


# read categories from arguments. e.g. "python assignment_classification.py BINNENLAND SPORT KUNST"
categories = list()
for arg in sys.argv[1:]:
	categories.append(arg)

# main
feats = read_files(categories)
high_info_words = high_information(feats, categories)
accuracyList = []

for N in range(10): # towards n-fold cross validation?
	train_feats, test_feats = split_train_test(feats)
	classifier = train(train_feats)
	accuracy = evaluation(classifier, test_feats, categories)
	accuracyList.append(accuracy)
	analysis(classifier)
	
lenList = 0
summed = 0
for number in accuracyList:
        lenList =  lenList + 1
        summed = summed + number
        print(number)
average = summed / lenList
print(average)
