##Classify each line of input
##Will be invoked as python3 percepclassify.py MODELFILE < data.in > data.out
##The label/class for each input will be the output

import pickle
import sys

##The feature_vector is the model that will be used to calculate the classes
##Testset is a list of sentnces that have to be tagged with the right class.

def classify(feature_vector,sentence):
	weights=dict()
	predicted_class=""
	prev_tag=predicted_class
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
	##return(predicted_class)		
	return predicted_class
def main():
	testset=list()
	predicted_values=list()
	modelfile=open(sys.argv[1],"rb")
	feature_vector=pickle.load(modelfile)
	modelfile.close()
	for sentence in sys.stdin:
		predicted_value=classify(feature_vector,sentence)
		print(predicted_value)
		sys.stdout.flush()
	
	return
	
if __name__=="__main__":
	main()	
