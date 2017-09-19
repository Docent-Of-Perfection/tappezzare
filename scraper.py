#!bin/bash/env python3
import requests, bs4, pprint
'''
redditUrl = "http://reddit.com/r/wallpapers"
redditRequest = requests.get(redditUrl)
redditRequest.raise_for_status()
'''
fourChanUrl = "http://4chan.org/wg/"
fourChanRequest = requests.get(fourChanUrl)
fourChanRequest.raise_for_status()

fourChanMarkup = bs4.BeautifulSoup(fourChanRequest.text,"lxml")

#Returns image urls from 4chan  in format image:thumbnail
def fourChanUrlStripper(fourChanArgs):
    output = []
    allContent = fourChanMarkup.select(".fileThumb")
    for link in allContent:
        # indicates the file has been deleted
        if "href" not in link.attrs:
            continue
        output.append([link.attrs['href'][2:],link.find('img').attrs['src'][2:]])
    pprint.pprint("Here is the output: \n " + str(output))
    print(str(len(output)) + " image URLs were scraped from 4chan")
