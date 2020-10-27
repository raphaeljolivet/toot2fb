#!/usr/bin/env python
import feedparser
from html2text import html2text

URL="https://mamot.fr/@RaphJ.rss"

feed = feedparser.parse(URL)

for entry in feed['entries'] :
    sum = entry['summary_detail']
    sum_value = html2text(sum.value) if sum.type == 'text/html' else sum.value

    print(entry)