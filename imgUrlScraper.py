#!/usr/bin/env python3

import requests, bs4, pprint

def dbug(stuff):
        print(stuff)
wgUrl= "http://4chan.org/wg/"
imageMaster = []
parentThreads = []
def getMarkup(url):
        request = requests.get(url)
        request.raise_for_status()
        markup = bs4.BeautifulSoup(request.text,"lxml")
        dbug("here is the server response: " + str(request))
        return markup

#run this against each full thread URL
def grabImgsFromPage(pageMarkup):
        appendToMaster = []
        subject = pageMarkup.select('.subject')[0].text
        appendToMaster.append(subject)
        fullResLinks = pageMarkup.select(".thread .fileText a")
        dbug(subject)
        for link in fullResLinks:
                appendToMaster.append(link['href'][2:])
                dbug("Appending " + link['href'][2:])
        imageMaster.append(appendToMaster)


#grab each 'click here' parent link on /wg/
def getAllLinks(markup):
        #eachParent = []
        clickHereLinks = markup.select('.summary .replylink')
        if clickHereLinks:
                dbug("ok")
        else:
                dbug("uh oh")
        for link in clickHereLinks:
                parentThreads.append("http://boards.4chan.org/wg/" + link['href'])


def loopThroughPages(url):
        dbug("Grabbing Home Page")
        markup = getMarkup(url)
        pageLinks = getAllLinks(markup)

        for i in range(2,11):
            url = "http://boards.4chan.org/wg/" + str(i)
            dbug("URL is " + url)
            markup = getMarkup(url)
            pageLinks = getAllLinks(markup)

loopThroughPages(wgUrl)
'''
#from parentThreads add to imageMaster
for link in parentThreads:
    markup = getMarkup(link)
    grabImgsFromPage(markup)
'''
def requestThenGrab(urls):
    for link in urls:
        markup = getMarkup(link)
        grabImgsFromPage(markup)

requestThenGrab(parentThreads)

#TODO: Quit thumbnailing subjects without fucking up pairing in other list items
def iterateNestedLists(lists):
    for sublist in lists:
        for idx,pic in enumerate(sublist):
            if pic[-4:] == '.jpg' or '.png':
                sublist[idx] += ':' + pic[:-4] + 's.jpg'
            else:
                del pic
iterateNestedLists(imageMaster)
pprint.pprint(imageMaster)
print(len(imageMaster))
