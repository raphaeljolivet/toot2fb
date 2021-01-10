
# Purpose

This small Flask web app is a filter to connect RSS Feed (from Mastodon) to Facebook, via IFFFT.
It splits a single RSS feed into 3 separate feeds :
* Text status only
* Images
* Links

It also adds the URL of the source, as per the [POSSE principle of Indie Web philosophy](https://indieweb.org/POSSE)

# Usage

## Server

Launch it locally for dev :
> flask main.py

Or set it up permanently with [PM2](https://pajaaleksic.com/deploying-python-flask-app-with-pm2-on-ubuntu-server-18-04/) or [UWSGI](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uswgi-and-nginx-on-ubuntu-18-04)

## URLs

> http://domain.tld/?url=[url]&filter=[text|link|image]

Query params
* **url** : URL of the source RSS feed
* **filter** : "text", "link" or "image"


# TODO

Add secret private ID for security
