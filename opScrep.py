#!/usr/bin/env python3
import bs4,requests,pprint,os.path

opSubjects = []
def makeRequest(requestTo):
	urlWgRequest = requests.get(requestTo)
	urlWgRequest.raise_for_status()
	markup = bs4.BeautifulSoup(urlWgRequest.text,"lxml")
	return markup

def miner(ore):
	specialOps = ore.select(".op .desktop .subject")
	for post in specialOps:
		if(post.text):
			opSubjects.append(post.text)
	
def pullSubjects():
	urlWg = "http://4chan.org/wg"
	mineThis = makeRequest(urlWg)
	miner(mineThis)

	for i in range(2,11):
		urlWg = "http://boards.4chan.org/wg/" + str(i)
		print(urlWg)
		mineThis = makeRequest(urlWg)
		miner(mineThis)

def appendToFile(filename):
	try:
		with open(filename, 'a') as fileObject:
			fileObject.write( "\n".join(opSubjects))
			fileObject.close()
	except: 
		print("Error writing the file")

pullSubjects()
#remove /wg/ sticky
del opSubjects[0]
appendToFile('subjects.txt')
pprint.pprint(opSubjects)
