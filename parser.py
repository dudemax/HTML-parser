import urllib2

def GetTagsData(html, tag):
	begS=0; endS=0; StagD=''; opent={'holder':0}
	begE=0; endE=0; EtagD=''; Data=''
	canParse=False
	myiter = iter(range(1, len(html)))
	for x in myiter:
		if html[x]=='<':
			compare=''
			for i in range(1, len(tag)+1):
				compare +=html[x+i]
			if tag == compare:
				print('tag=compare')
				if (tag in opent)==False:
					opent[tag]=0
				opent[tag]+=1
				while html[x]!='>':
					StagD+=html[x]
					x+=1
					next(myiter,None)
					canParse=False
				canParse=True
				continue
		if html[x]=='<' and html[x+1]=='/':
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
	
def GetTableRows():
	begS=0; endS=0; StagD=''; opent={'holder':0}
	begE=0; endE=0; EtagD=''; Data=''
	canParse=False
	myiter = iter(range(1, len(html)))
	for x in myiter:
		if html[x]=='<':
			compare=''
			for i in range(1, len('td')+1):
				compare +=html[x+i]
			if tag == compare:
				print('tag=compare')
				if ('td' in opent)==False:
					opent[tag]=0
				opent[tag]+=1
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
			if tag == compare:
				opent[tag]-=1
				x=x+i+1
				while html[x]!='>':
					x+=1
				canParse=False
		if canParse:
			Data+=html[x];
	return Data
	

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
req = urllib2.Request('https://www.socks-proxy.net/', headers=hdr)
response = urllib2.urlopen(req)
html = response.read()
decision='y'
while decision=='y':
	tag=raw_input("Enter tag: ")
	tagD=GetTagsData(html,tag)
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

