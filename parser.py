import urllib2

def GetTagsData(html, tag):
	begS=0; endS=0; StagD=''; opent={'holder':0}
	begE=0; endE=0; EtagD=''; Data=''
	for x in range(1, len(html)):
		if(html[x-1]=='<'):
			compare=''
			for i in range(0, len(tag)):
				compare +=html[x+i]
			if tag == compare:
				if (tag in opent)==False:
					opent[tag]=0
				opent[tag]+=1
				begS=x+i+1
				x=x+i+1
				while html[x]!='>':
					StagD+=html[x]
					x+=1
				endS=x
				print(opent)
		elif html[x-2]=='<' and html[x-1]=='/':
			compare=''
			for i in range(0, len(tag)):
				compare +=html[x+i]
			if tag == compare:
				opent[tag]-=1
				begE=x+i+1
				x=x+i+1
				while html[x]!='>':
					EtagD+=html[x]
					x+=1
				endE=x
				print(opent)
				Data=Data[:-2]
				return Data
		Data+=html[x];

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
req = urllib2.Request('https://www.socks-proxy.net/', headers=hdr)
response = urllib2.urlopen(req)
html = response.read()
tag=raw_input("Enter tag: ")
tagD=GetTagsData(html,tag)
print(tagD)

#print(html)

