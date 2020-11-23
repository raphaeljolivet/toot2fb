#!/usr/bin/env python
import feedparser
from html2text import HTML2Text
from bs4 import BeautifulSoup
from rfeed import *
from datetime import datetime
from time import mktime
from flask import Flask
from flask import request, Response

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

def transform_rss(filter=None) :
    items= []
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
        summary_html = "<br/>".join(summary_txt.splitlines())

        if filter is not None and type != filter :
            continue

        items.append(Item(
            title=entry.title,
            link=out_entry_link,
            description=summary_html,
            guid=Guid(entry.guid),
            pubDate=datetime.fromtimestamp(mktime(entry.published_parsed))
        ))


    outfeed = Feed(
        title = feed.feed.title,
        link = feed.feed.link,
        description = feed.feed.description,
        items = items)
    return outfeed




app = Flask(__name__)

@app.route('/')
def entry_point():
    res = transform_rss(request.args.get("filter"))
    return Response(res.rss(), mimetype='text/xml')

if __name__ == '__main__':
    app.run(debug=True)