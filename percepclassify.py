##Classify each line of input
##Will be invoked as python3 percepclassify.py MODELFILE
##The label(class) for each sentence will be the output

import pickle
import sys


def classify(sentence):
	weights=dict()
	maxi=0
	for classes in feature_vector:
		weights[classes]=0
		words=sentence.split()
		for word in words:
			if word in feature_vector[classes]:
				##if the word has a non-zero value add it
				weights[classes]+=feature_vector[classes][word]
		##retrieve the max label
		if(maxi<=weights[classes]):
			maxi=weights[classes]
			predicted_class=classes
	print(predicted_class)
	return
	
modelfile=open(sys.argv[1],"rb")
feature_vector=pickle.load(modelfile)
modelfile.close()
while(1):
	sentence=input()
	classify(sentence)
	

	
	
	
