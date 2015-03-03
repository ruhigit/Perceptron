##Classify each line of input
##Will be invoked as python3 postag.py MODELFILE <data.in >data.out
##The label for each input will be the output


import sys
import re
import pickle
import codecs

def classify(feature_vector,testset):
	weights=dict()
	predicted_values=list()
	predicted_class=""
	for sentence in testset:
		prev_tag=predicted_class
		
		sentence+=" prev_tag:"+prev_tag
		##print(sentence)
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
		##print(predicted_class)
		predicted_values.append(predicted_class)		
	return predicted_values

def wordshape(curr):
	wshape=""
	for char in curr:
		if char.islower():
			wshape+='a'
			wshape=re.sub('aa','a',wshape)
		elif char.isupper():
			wshape+='A'
			wshape=re.sub('AA','A',wshape)
		elif char.isdigit():
			wshape+='9'
			wshape=re.sub('99','9',wshape)
		else:
			wshape+='-'
			wshape=re.sub('--','-',wshape)
	
	return wshape

def format(testset):
	op=list()
	for line in testset:
		words=line.split()
		len_sentence=len(words)
		for index,word in enumerate(words):
				
			curr=words[index]
				
			if index==0:
				##if first word then previous tag is BOS
				prev="BOS"
			else:
				prev=words[index-1]
				
			if index==len_sentence-1:
				##if last word then next tag is EOS
				next="EOF"
			else:
				next=words[index+1]
				
			suffix3=curr[len(curr)-3:]
			suffix2=curr[len(curr)-2:]
			wshape=wordshape(curr)
			sentence="prev:%s curr:%s next:%s suffix3:%s suffix2:%s wshape:%s" %(prev,curr,next,suffix3,suffix2,wshape)

			op.append(sentence)

	return op
			
def main():
	
	counter=0
	predicted_classes=list()
	modelfile=open(sys.argv[1],"rb")
	feature_vector=pickle.load(modelfile)
	modelfile.close()

	sys.stdin = codecs.getreader('utf8')(sys.stdin.detach(), errors='ignore')
	testset = sys.stdin.readlines()
	testlist=format(testset)

	predicted_classes=classify(feature_vector,testlist)
	for line in testset:
		tagged_line=""
		words=line.split()
		for word in words:	
			word+="/"+predicted_classes[counter]
			counter+=1
			tagged_line+=word+" "
		sys.stdout.flush()
		print(tagged_line)	
	return

if __name__=="__main__":
	main()
	
