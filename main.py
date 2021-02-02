#!/usr/bin/env python
import feedparser
from html2text import HTML2Text
from bs4 import BeautifulSoup
from rfeed import *
from datetime import datetime
from time import mktime
from flask import Flask
from flask import request, Response

TYPE_TEXT = "text"
TYPE_LINK = "link"
TYPE_IMAGE = "image"


html2text = HTML2Text()
html2text.ignore_links = True

def transform_rss(url, filter=None) :
    items= []
    feed = feedparser.parse(url)

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
                if 'video' in link.type :
                    # VIDEO upload is not supported by IFTTT : let's share link to video
                    type = TYPE_LINK
                    out_entry_link = link.href
                    break

        if summary.type == 'text/html' :

            html = BeautifulSoup(summary.value, 'html.parser')

            for link in html.findAll('a'):
                if not (link.get("class") and "mention" in link.get("class")) and type == TYPE_TEXT:
                    type = TYPE_LINK
                    out_entry_link = link.get('href')
                    link.extract()
                    break

            summary_html = html.prettify()

        else :
            summary_txt = summary.value.splitlines()
            summary_html = "<br/>".join(summary_txt.splitlines())

        summary_html += "<br/>\n[transféré depuis %s]" % entry_link
        summary_html = summary_html.strip()

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
    filter = request.args.get("filter")
    url = request.args.get("url")
    res = transform_rss(url, filter)
    return Response(res.rss(), mimetype='text/xml')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True, threaded=True)