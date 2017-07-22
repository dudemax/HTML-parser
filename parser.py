import urllib2
from collections import defaultdict
import checker

def GetTagsData(html, tag, attrs): #returns data between defined open and close tags
	begS=0; endS=0; StagD=''; opent=dict()
	EtagD=''; Data=''; attrM=False;
	canParse=False
	myiter = iter(range(1, len(html)))
	for x in myiter:
		if html[x]=='<' and html[x+1]!='/' and html[x+1]!='!':
			compare=''
			for i in range(1, len(tag)+1):
				compare +=html[x+i]
			#print(compare)
			#print(tag)
			if tag == compare:
				#print('here')
				if (tag in opent)==False:
					opent[tag]=0
				opent[tag]+=1
				while html[x]!='>':
					StagD+=html[x]
					x+=1
					next(myiter,None)
					canParse=False
				#print(StagD)
				#if len(attrs)>0:
				for attr in attrs:
					if StagD.find(attr+"=")!=-1:
						#print('ble')
						if StagD[StagD.find(attr+"=")+len(attr+"=")]!="\"" and StagD[StagD.find(attr+"=")+len(attr+"=")]!='\'':
							attrCompare=''
							#print attrs
							for attri in range(0,len(attrs[attr])):
								attrCompare+=StagD[StagD.find(attr+"=") + len(attr+"=") + attri]
							#print(StagD[StagD.find(attr+"=")+len(attr+"=")])
							#print(attrCompare)
							if attrCompare==attrs[attr]:
								attrM=True
						else:
							attrCompare=''
							for attri in range(0,len(attrs[attr])):
								attrCompare+=StagD[StagD.find(attr+"=") + len(attr+"=")+1 + attri]
							if attrCompare==attrs[attr]:
								attrM=True
				else:
					attrM=True
				if attrM:
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
	
	
def GetTableRows(html,rowsC): #return list of lists consists of all table rows
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

def CommandRecognize(Mtag, commands): #Recognize tag input e.g. "table -c SomeClass" or "div --id=SomeId"
	tdDict={'rws':-1, 'adr':-1, 'port':-1, 'type':-1}
	AllDict={}
	#print("Command = "+command+"\nArg = "+arg)
	for i in commands:
		print("Command = "+i+"\nArg = "+commands[i])
	if Mtag=='td':
		for i in commands:
			if tdDict[i]!=None:
				tdDict[i]=commands[i]
		if tdDict[rws]!=-1:
			table=GetTableRows(html, tdDict['rws'])
			SummarizeRows(table, tdDict['addr'], tdDict['port'], tdDict['Ptype'])
		else:
			print "Error, wrong/undefined Rows Count"
	else:
		for i in commands:
			AllDict[i]=commands[i]
		table = GetTagsData(html, Mtag, AllDict)
		global html
		html=table
		print table
				
def SummarizeRows(table, addr, port, Ptype): #Format output to file "type address port"
	f = open('out.txt', 'a')
	for i in range(0, len(table[1])):
		if Ptype!=None and Ptype !=-1:
			if addr!=None and addr!=-1:
				if port!=None and port!=-1:
					f.write(table[Ptype][i].lower()+' '+table[addr][i]+' '+table[port][i]+'\n')
		else:
			f.write('http'+' '+table[addr][i]+' '+table[port][i]+'\n')
		#print(table[Ptype][i].lower()+' '+table[addr][i]+' '+table[port][i])
		#checker.proxyList.append(tagD[0][i]+':'+tagD[1][i])
		#print(tagD[0][i].lower());
	#checker.LoopCheck()
	#print(tagD)
	f.close()
	
def ParseCommand(tag):
	dictionary=dict()
	tagparsed = False
	Mtag=''
	tagiter = iter(range(0, len(tag)))
	#i=0
	for i in tagiter:
		if tagparsed==False and tag[i]!=' ' and i!=len(tag):
			Mtag+=tag[i]
			#print(str(i)+" "+tag[i])
			#next(tagiter)
			#i+=1
		else:
			tagparsed=True
		if tagparsed:
			if tag[i]=='-':
				if tag[i+1]=='-':
					next(tagiter)
					command=''
					while tag[i+2]!='=':
						command+=tag[i+2]
						i+=1
					arg=''
					while tag[i+3]!=' ':
						arg+=tag[i+3]
						if (i+4)!=len(tag):
							i+=1
						else:
							break
					#CommandRecognize(command, arg)
					dictionary[command]=arg
				else:
					command=''
					while tag[i+1].isspace()==False and (i+1)!=len(tag):
						command+=tag[i+1]
						if tag[i+1]==' ':
							print "Fucker"
						next(tagiter, None)
						i+=1
					arg=''
					while tag[i+2].isspace()==False and (i+2)!=len(tag):
						arg+=tag[i+2]
						if (i+3)!=len(tag):
							i+=1
						else:
							break
					#CommandRecognize(command, arg)
					dictionary[command]=arg
	print Mtag
	print dictionary
	CommandRecognize(Mtag,dictionary)
	

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
#req = urllib2.Request('https://www.socks-proxy.net/', headers=hdr)
#req = urllib2.Request('http://freeproxylists.net/', headers=hdr)
req = urllib2.Request('http://useragentstring.com/pages/useragentstring.php?typ=Browser', headers=hdr)
response = urllib2.urlopen(req)
html = response.read()
decision='y'
f = open('out.txt', 'w')
f.write('')
f.close()
while decision=='y':
	tag=raw_input("Enter tag: ")
	ParseCommand(tag)
		#tagD=GetTableRows(html,10)

		#tagD=GetTagsData(html,tagS,cl)
	#for i in range(0, len(tagD[1])):
		#f.write(tagD[2][i].lower()+' '+tagD[0][i]+' '+tagD[1][i]+'\n')
		#print(tagD[2][i].lower()+' '+tagD[0][i]+' '+tagD[1][i])
		#checker.proxyList.append(tagD[0][i]+':'+tagD[1][i])
		#print(tagD[0][i].lower());
	#checker.LoopCheck()
	#print(tagD)
	decision=raw_input("Parse more? (y/n) ")
	if decision!='y' and decision!='n':
		print ("Are U kidding at me?!")
		exit("Fuck")
	elif decision=='n':
		print ("Good Bye!)")
		exit()
