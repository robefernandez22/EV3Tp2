# -*- coding: utf-8 -*-
from flask import Flask
import feedparser
from flask import render_template
from flask import request
from flask import make_response
from lxml import etree
import urllib2

app= Flask(__name__)

RSS_FEED = { 'elp':'http://ep00.epimg.net/rss/tags/ultimas_noticias.xml',
             'bbc':'http://feeds.bbci.co.uk/news/rss.xml',
             'lav':'http://www.lavanguardia.com/mvc/feed/rss/politica',
             'cnn':'http://rss.cnn.com/rss/edition.rss',
             'abc':'http://sevilla.abc.es/rss/feeds/Sevilla_Sevilla.xml',
             'elm':'http://estaticos.elmundo.es/elmundo/rss/portada.xml'
}
Titles = {'elp':'El Pais: Ultimas noticas',
          'bbc':'BBC headlines',
          'lav':u'La Vanguardia: Política',
          'cnn':'CNN headlines',
          'abc':'ABC: Sevilla',
          'elm':'El Mundo'
}

articles = {}
articles['elp'] = feedparser.parse(RSS_FEED['elp'])['entries'][:5]
articles['bbc'] = feedparser.parse(RSS_FEED['bbc'])['entries'][:5]
articles['lav'] = feedparser.parse(RSS_FEED['lav'])['entries'][:5]
articles['cnn'] = feedparser.parse(RSS_FEED['cnn'])['entries'][:5]
articles['abc'] = feedparser.parse(RSS_FEED['abc'])['entries'][:5]
articles['elm'] = feedparser.parse(RSS_FEED['elm'])['entries'][:5]


@app.route("/imagenes")
def get_imagenes():
  ns={"Atom" : "http://www.w3.org/2005/Atom"}
  parser=etree.XMLParser()
  tree=etree.parse(urllib2.urlopen('https://api.flickr.com/services/feeds/photos_public.gne?tags=sevilla'),parser)
  images = tree.xpath('//Atom:entry/Atom:title', namespaces=ns)
  return render_template("home.html", images=images)

@app.route("/elpais")
def get_elpais():
  new = []
  url = 'http://ep00.epimg.net/rss/tags/ultimas_noticias.xml'
  news = feedparser.parse(url)['entries']
  return render_template("home1.html", news=news)


@app.route("/")
def get_news():
  return render_template("home.html", articles=articles,titles=Titles)

if __name__ == '__main__':
  app.run(port=5300,debug=True)
