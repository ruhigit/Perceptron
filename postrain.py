import sys
import re
sys.path.insert(0, "..")
from perceplearn import perceptron

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
def format_file(inputfile):
	ip=open(inputfile,'r')
	op=list()
	for line in ip:
		words=line.split()
		len_sentence=len(words)
		for index,word in enumerate(words):
			
			curr=words[index][:words[index].rfind('/')]
			
			if index==0:
				##if first word then previous tag is BOS
				prev="BOS"
				prev_tag="PTAG"
			else:
				prev=words[index-1][:words[index-1].rfind('/')]
				prev_tag=words[index-1][words[index-1].rfind('/')+1:]
			if index==len_sentence-1:
				##if last word then next tag is EOS
				next="EOF"
			else:
				next=words[index+1][:words[index+1].rfind('/')]
			suffix3=curr[len(curr)-3:]
			suffix2=curr[len(curr)-2:]
			wshape=wordshape(curr)
			sentence="prev:%s curr:%s next:%s suffix3:%s suffix2:%s wshape:%s prevtag:%s" %(prev,curr,next,suffix3,suffix2,wshape,prev_tag)
			tag=words[index][words[index].rfind('/')+1:]
			sentence=tag+" "+sentence+"\n"
			op.append(sentence)
			##print(sentence)
	ip.close()
	return op
			
def main():
	
	trainingset=format_file(sys.argv[1])
	##print(len(trainingset))
	
	perceptron(trainingset,sys.argv[2])
	return
	
if __name__=="__main__":
	main()
