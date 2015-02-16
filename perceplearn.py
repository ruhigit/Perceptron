##This is Averaged Perceptron classifier. Will be invoked as:
##python3 perceplearn.py TRAININGFILE MODELFILE
##where trainingfile contains a label and document features. Each line represnts one training example.
##In this program we compute the dot product of the features and it's weights for every document.
##We assume all weights to be 0 initially, andput only updted weights of features for each class
##The output z is compared to the label y. If they are not equal the weights of those features are updated.

import sys
import pickle
	
def perceptron(ip,op):
	i=0
	j=0
	feature_vector=dict() ##words of the training files are the features here.
	weights=dict() ##has entries equal to number of classes, and contains the weight
	trainingset=open(ip,'r')
	modelfile=open(op,'wb')
	##number of iterations
	while(i!=3):
		##print("***************")
		trainingset=open(ip,'r')
		for file in trainingset:
			words=file.split()
			#Decide the default class in case of equal weights to be the first label in training file
			if(j==0 and i==0):
				predicted_class_default=words[0]
			maxi=0##to predict max value
			predicted_class=predicted_class_default
			for classes in weights:
				weights[classes]=0
			j+=1
			for index,word in enumerate(words):
				## If index is 0 then store the class name
				class_name=words[0]##first word is the class name in traning file
				
				if index==0:
					##The first label is the default predicted class in case of same values
					##print("classname:",class_name)
					##only first iteration will be enough to predict the names of classes
					if(i==0):
						##check if class has been detected before
						if class_name not in feature_vector :
							##if class is new and does not exist already add it to list of class names
							feature_vector[class_name]=dict()
							weights[class_name]=0
							##if class already exists just move ahead
				else:
						##calculate z(dot product) for each class
					for classes in feature_vector:
						if word in feature_vector[classes]:
							##if the word has a non-zero value add it
							weights[classes]+=feature_vector[classes][word]
						##retrieve the max label
						if(maxi<weights[classes]):
							maxi=weights[classes]
							predicted_class=classes
						elif(weights[classes]==0):
							predicted_class=predicted_class_default
			
			##print("Weight_vector:",weights)
			##print("Predicted class:",predicted_class)
			##If mistake has been made update the values of those features
			
			if(class_name!=predicted_class):
				for index,word in enumerate(words):
					if(index!=0):
						##if that feature is absent create 1
						if word not in feature_vector[class_name]:
							feature_vector[class_name][word]=0
							##Update weights
						feature_vector[class_name][word]+=1
						if word not in feature_vector[predicted_class]:
								feature_vector[predicted_class][word]=0
						feature_vector[predicted_class][word]-=1
		print("Feature_vector:",feature_vector)
		trainingset.close()
		i+=1
		##shuffle the training examples for better accuracy
		##code to decide number of iterations
	##Average the weights
	##Return the final weights into model file
	pickle.dump(feature_vector,modelfile)
	modelfile.close()
	return
def main():
	perceptron(sys.argv[1],sys.argv[2]);
	return
if __name__=="__main__":
	main()
