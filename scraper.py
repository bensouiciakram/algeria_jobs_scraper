import scrapy 
from scrapy.spiders import CrawlSpider
from scrapy.crawler import CrawlerProcess 
from scrapy import Request 
from itemloaders.processors import TakeFirst
from scrapy.loader import ItemLoader
from re import findall,sub
from math import ceil 
from scrapy.shell import inspect_response
from urllib.parse import quote 
from scrapy.utils.response import open_in_browser
import json 
from math import ceil 
import pickle 
import pandas as pd 
from urllib.parse import urlparse 
from playwright.sync_api import sync_playwright,TimeoutError 
from parsel import Selector 
from pathlib import Path 

class DetailsItem(scrapy.Item):
    pass 

class InfosSpider(scrapy.Spider):
    name = 'extractor'  


    
process = CrawlerProcess(
    {
        'FEED_URI':Path('.').parent.joinpath('output.csv'),
        'FEED_FORMAT':'csv',
        'HTTPCACHE_ENABLED' : True,
    }
)



process.crawl(InfosSpider)
process.start()
