# -*- coding: utf-8 -*-
"""

@author: Jonathan Hill
"""

from bs4 import BeautifulSoup
import urllib2
import re
import pandas as pd
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

PARENT_URL = "https://en.wikipedia.org/wiki/Category:Science"
CAT_CLASS = "CategoryTreeLabel"

def main():
    name = 'en.wikipedia.org'
    allowed_domains = ["https://en.wikipedia.org"]
    start_urls = ["https://en.wikipedia.org/wiki/Category:Science"]
    
    rules = (Rule(LinkExtractor(allow=("index\d00\.html", ),restrict_xpaths=('//a[@class="button next"]',))
    , callback="parse_items", follow= True),
    )
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
def traverse(url, tree=[[]], level=0, subNumber=0):
    
    url = getLinks
    if len(links)>0:
        if level !=0: tree = tree.append([])
        # child categories found, append next level
        for link in links[subNumber:]:
            
            print link.text+"\n"+link['href']
            
            tree[level].append({ "name": link.text, "link": link['href'] })
            level+=1
            traverse(tree,level,0,link['href'])
    else:
        level-= 1
        subNumber += 1
        traverse(url, tree, level, subNumber)
    return tree

def getLinks(url):
    html_page = urllib2.urlopen(url)
    soup = BeautifulSoup(html_page, "lxml")
    return soup.find_all("a", class_=CAT_CLASS)
        
if __name__ == "__main__":
    main()