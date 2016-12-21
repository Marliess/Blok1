import sys
#import nltk.classify
#from nltk.stem.porter import *


def improve():
    file = open("label.txt","r")
    #stemmer = PorterStemmer()
    #lowercase
    for line in file:
        words = line.lower()
        print(words,end="")
        for word in line:
            words = stemmer.stem(word)

improve()
