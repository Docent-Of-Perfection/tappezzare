#!/usr/bin/env python3
import argparse
from scraper import fourchan_url_stripper, DEFAULT_URL

def generate_fullres_tags(board_url):
    tagstext = '<img style="width: 30%; height: auto;" src="https://{}">'
    return [tagstext.format(p[0]) for p in fourchan_url_stripper(board_url)]

def generate_thumb_tags(board_url):
    tagstext = '<img src="https://{}">'
    return [tagstext.format(p[0]) for p in fourchan_url_stripper(board_url)]

def generate_nested_tags(board_url):
    tagstext = '<a href="{}"><img src="https://{}"></a>'
    return [tagstext.format(p[0],p[1]) for p in fourchan_url_stripper(board_url)]

generator_func = {"fullres": generate_fullres_tags, "f": generate_fullres_tags,
                  "thumb": generate_thumb_tags, "t": generate_thumb_tags,
                  "nested": generate_nested_tags, "n": generate_nested_tags}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="generate img tags for copy-paste")
    parser.add_argument('-u', '--url', nargs='*', default=[DEFAULT_URL],
                        help="list of urls to scrape")
    parser.add_argument('-t', '--tagstyle', nargs=1, help='style of tag to generate',
                        choices=["fullres", "f", "thumb", "t", "nested", "n"],
                        default="f")
    args = parser.parse_args()
    
    for url in args.url:
        tags = generator_func[args.tagstyle](url)
        print("<!-- {} -->".format(url))
        for tag in tags:
            print(tag)

