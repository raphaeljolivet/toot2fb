#!/usr/bin/env python
import feedparser
from html2text import html2text
import facebook

URL="https://mamot.fr/@RaphJ.rss"
APP_ID="370919417317291"
APP_SECRET="22add9d6d0002f23800c5a7b7536de3c"
PAGE_ID="112264450137701"

feed = feedparser.parse(URL)

for entry in feed['entries'] :
    sum = entry['summary_detail']
    sum_value = html2text(sum.value) if sum.type == 'text/html' else sum.value

    print(entry)


token = facebook.GraphAPI().get_app_access_token(APP_ID, APP_SECRET)
graph = facebook.GraphAPI(token)
page = graph.get_object(PAGE_ID)

print(page)