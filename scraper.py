#!/usr/bin/env python3
import re, sys, requests, bs4, pprint

# redditUrl = "http://reddit.com/r/wallpapers"
# redditRequest = requests.get(redditUrl)
# redditRequest.raise_for_status()

DEFAULT_URL = "http://4chan.org/wg/"

# Returns image urls from 4chan  in format image:thumbnail
def fourchan_url_stripper(board_url):
    fourchan_request = requests.get(board_url)
    fourchan_request.raise_for_status()
    fourchan_markup = bs4.BeautifulSoup(fourchan_request.text, "lxml")
    
    output = []
    all_content = fourchan_markup.select(".fileThumb")
    # exclude sticky and FAQ  images if the landing page for wg
    if board_url == "http://4chan.org/wg/":
        all_content = all_content[2:]
    for link in all_content:
        # indicates the file has been deleted
        if "href" not in link.attrs:
            continue
        fullres, thumb = link.attrs['href'][2:], link.find('img').attrs['src'][2:]
        # checking thumbnail type unnecessary, because all thumbnails are .jpg
        if not re.search("\.(jpe?g|gif|png)$", fullres):
            continue
        output.append([fullres, thumb])
    return output

def main():
    if len(sys.argv) == 1:
        wallpaper_board_url = DEFAULT_URL
    else:
        wallpaper_board_url = sys.argv[1]
    image_urls = fourchan_url_stripper(wallpaper_board_url)
    pprint.pprint("Here is the output: \n " + str(image_urls))
    print(str(len(image_urls)) + " image URLs were scraped from 4chan")


if __name__ == '__main__':
    main()
    