import sys
import re
import codecs
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
	
	##print("Ip:",inputfile)
	ip=open(inputfile,'r',errors="ignore")
	op=list()
	for line in ip:
		words=line.split()
		len_sentence=len(words)
		for index,word in enumerate(words):
			
			curr=words[index][:words[index].rfind('/')]
			curr_tag=curr[curr.rfind('/')+1:]
			curr=curr[:curr.rfind('/')]
			
			if index==0:
				##if first word then previous tag is BOS
				prev="BOS"
				prev_tag="PVTAG"
			else:
				prev=words[index-1][:words[index-1].rfind('/')]
				prev_tag=prev[prev.rfind('/')+1:]
				prev=prev[:prev.rfind('/')]
			if index==len_sentence-1:
				##if last word then next tag is EOS
				next="EOF"
				next_tag="PVTAG"
				
			else:
				next=words[index+1][:words[index+1].rfind('/')]
				next_tag=next[next.rfind('/')+1:]
				next=next[:next.rfind('/')]

			wshape=wordshape(curr)
			sentence="prev:%s curr:%s next:%s prev_tag:%s curr_tag:%s next_tag:%s wshape:%s" %(prev,curr,next,prev_tag,curr_tag,next_tag,wshape)
			tag=words[index][words[index].rfind('/')+1:]
			sentence=tag+" "+sentence
			##print(sentence)
			op.append(sentence)
		
			
	ip.close()
	return op
			
def main():
	
	trainset=format_file(sys.argv[1])
	##print(trainset)
	##print(len(trainset))
	perceptron(trainset,sys.argv[2])
	return
	
if __name__=="__main__":
	main()
