#!/usr/bin/env python
import feedparser
from html2text import HTML2Text
from bs4 import BeautifulSoup
import facebook

URL="https://mamot.fr/@testrjo.rss"
APP_ID="370919417317291"
APP_SECRET="22add9d6d0002f23800c5a7b7536de3c"
PAGE_ID="112264450137701"

feed = feedparser.parse(URL)

TYPE_TEXT = "text"
TYPE_LINK = "link"
TYPE_IMAGE = "image"


html2text = HTML2Text()
html2text.ignore_links = True

for entry in feed['entries'] :

    type = TYPE_TEXT

    summary = entry['summary_detail']
    entry_link = entry["link"]
    out_entry_link = entry_link

    if 'links' in entry :
        for link in entry['links'] :
            if 'image' in link.type :
                type = TYPE_IMAGE
                out_entry_link = link.href
                break

    if summary.type == 'text/html' :

        html = BeautifulSoup(summary.value, 'html.parser')
        summary_txt = html2text.handle(summary.value)

        for link in html.findAll('a'):
            if not (link.get("class") and "mention" in link.get("class")) :
                type = TYPE_LINK
                out_entry_link = link.get('href')
                break

    else :
        summary_txt = summary.value



    summary_txt += "\n[transféré depuis %s]" % entry_link
    print("type", type)
    print("out_link", out_entry_link)
    print("text", summary_txt)
    print("\n\n")

"""
token = facebook.GraphAPI().get_app_access_token(APP_ID, APP_SECRET)
graph = facebook.GraphAPI(token)
page = graph.get_object(PAGE_ID)
print(page)"""