##Classify each line of input
##Will be invoked as python3 postag.py MODELFILE <data.in >data.out
##The label for each input will be the output


import sys
import re
import pickle
import codecs
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
def classify(feature_vector,testset):
	weights=dict()
	predicted_values=list()
	for sentence in testset:
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

def format(ip):
	
	op=list()
	for line in ip:
		words=line.split()
		len_sentence=len(words)
		for index,word in enumerate(words):
			##print(word)
			curr=words[index]
			curr_tag=curr[curr.rfind('/')+1:]
			curr=curr[:curr.rfind('/')]
			
			if index==0:
				##if first word then previous tag is BOS
				prev="BOS"
				prev_tag="PVTAG"
			else:
				prev=words[index-1]
				prev_tag=prev[prev.rfind('/')+1:]
				prev=prev[:prev.rfind('/')]

			if index==len_sentence-1:
				##if last word then next tag is EOS
				next="EOF"
				next_tag="PVTAG"
			else:
				next=words[index+1]
				next_tag=next[next.rfind('/')+1:]
				next=next[:next.rfind('/')]
			wshape=wordshape(curr)
			sentence="prev:%s curr:%s next:%s prev_tag:%s curr_tag:%s next_tag:%s wshape:%s" %(prev,curr,next,prev_tag,curr_tag,next_tag,wshape)
			##print(sentence)
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
	##print(testset)
	testlist=format(testset)
	##print(testlist)
	predicted_classes=classify(feature_vector,testlist)
	##print(predicted_classes)
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
	
