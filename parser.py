import urllib2
from collections import defaultdict
import checker

def GetTagsData(html, tag, cl):
	begS=0; endS=0; StagD=''; opent={'holder':0}
	EtagD=''; Data=''; clM=False;
	canParse=False
	myiter = iter(range(1, len(html)))
	for x in myiter:
		if html[x]=='<' and html[x+1]!='/' and html[x+1]!='!':
			compare=''
			for i in range(1, len(tag)+1):
				compare +=html[x+i]
			print(compare)
			#print(tag)
			if tag == compare:
				print('here')
				if (tag in opent)==False:
					opent[tag]=0
				opent[tag]+=1
				while html[x]!='>':
					StagD+=html[x]
					x+=1
					next(myiter,None)
					canParse=False
				print(StagD)
				if cl!=None:
					if StagD.find('class=')!=-1:
						print('ble')
						if StagD[StagD.find('class=')+6]!="\"" and StagD[StagD.find('class=')+6]!='\'':
							clCompare=''
							for ci in range(0,len(cl)):
								clCompare+=StagD[StagD.find('class=') + 6 + ci]
							print(StagD[StagD.find('class=')+6])
							print(clCompare)
							if clCompare==cl:
								clM=True
						else:
							clCompare=''
							for ci in range(0,len(cl)):
								clCompare+=StagD[StagD.find('class=') + 7 + ci]
							if clCompare==cl:
								clM=True
				else:
					clM=True
				if clM:
					canParse=True
				continue
		if html[x]=='<' and html[x+1]=='/' and canParse:
			compare=''
			for i in range(2, len(tag)+2):
				compare +=html[x+i]
			if tag == compare:
				opent[tag]-=1
				x=x+i+1
				while html[x]!='>':
					x+=1
				canParse=False
		if canParse:
			Data+=html[x];
	return Data
	
	
def GetTableRows(html,rowsC):
	begS=0; endS=0; StagD=''; opent={'holder':0}
	begE=0; endE=0; EtagD=''; Data=''
	d = defaultdict(list)
	canParse=False; rowsI=0
	myiter = iter(range(1, len(html)))
	for x in myiter:
		if html[x]=='<':
			compare=''
			for i in range(1, len('td')+1):
				compare +=html[x+i]
			if 'td' == compare:
				if ('td' in opent)==False:
					opent['td']=0
				opent['td']+=1
				while html[x]!='>':
					StagD+=html[x]
					x+=1
					next(myiter,None)
					canParse=False
				canParse=True
				continue
		if html[x]=='<' and html[x+1]=='/':
			compare=''
			for i in range(2, len('td')+2):
				compare +=html[x+i]
			if 'td' == compare:
				opent['td']-=1
				x=x+i+1
				while html[x]!='>':
					x+=1
				canParse=False
				if rowsI+1<rowsC:
					d[rowsI].append(Data)
					Data=''
					rowsI+=1
				else:
					d[rowsI].append(Data)
					Data=''
					rowsI=0
		if canParse:
			Data+=html[x];
	return d

def Decode(text):
	return urllib.unquote(text).decode('utf8')
	
	

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
#req = urllib2.Request('https://www.socks-proxy.net/', headers=hdr)
req = urllib2.Request('http://freeproxylists.net/', headers=hdr)
response = urllib2.urlopen(req)
html = response.read()
decision='y'
f = open('out.txt', 'w')
f.write('')
f.close()
f = open('out.txt', 'a')
while decision=='y':
	tag=raw_input("Enter tag: ")
	if tag=='td':
		tagD=GetTableRows(html,10)
	else:
		if tag.find('-c=')!=-1:
			ti=tag.find('-c=')+3
			cl=''
			print(tag+' '+str(len(tag)))
			while ti<len(tag):
				print(tag[ti])
				#print(ti)
				cl+=tag[ti]
				print(ti)
				ti+=1
		tagi=0; tagS=''
		while tag[tagi]!=' ':
			tagS+=tag[tagi]
			tagi+=1
		print(tagS+' '+cl)
		tagD=GetTagsData(html,tagS,cl)
	#for i in range(0, len(tagD[1])):
		#f.write(tagD[2][i].lower()+' '+tagD[0][i]+' '+tagD[1][i]+'\n')
		#print(tagD[2][i].lower()+' '+tagD[0][i]+' '+tagD[1][i])
		#checker.proxyList.append(tagD[0][i]+':'+tagD[1][i])
		#print(tagD[0][i].lower());
	#checker.LoopCheck()
	print(tagD)
	decision=raw_input("Parse more? (y/n) ")
	if decision!='y' and decision!='n':
		print ("Are U kidding at me?!")
		exit("Fuck")
	elif decision=='n':
		print ("Good Bye!)")
		exit()
	else:
		html=tagD
f.close()
