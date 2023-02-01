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
    title = scrapy.Field(
        output_processor=TakeFirst()
    )
    work_place = scrapy.Field(
        output_processor=TakeFirst()
    )
    expiration_date = scrapy.Field(
        output_processor=TakeFirst()
    )
    applicant_level = scrapy.Field(
        output_processor=TakeFirst()
    )
    section = scrapy.Field(
        output_processor=TakeFirst()
    )
    number_of_available_jobs = scrapy.Field(
        output_processor=TakeFirst()
    )
    contracts_type = scrapy.Field(
        output_processor=TakeFirst()
    ) 
    description = scrapy.Field(
        output_processor=TakeFirst()
    )
    job_url = scrapy.Field(
        output_processor=TakeFirst()
    )

class InfosSpider(scrapy.Spider):
    name = 'extractor'  
    config = pickle.load(open('config.pkl','rb'))

    def __init__(self,keyword):
        self.keyword = keyword 

    def start_requests(self):
        for domain in self.config:
            search_template = self.config[domain]['search_template']
            yield Request(
                search_template.format(self.keyword),
                callback=self.parse_jobs,
                meta={
                    'search_template':search_template,
                    'domain':domain
                }
            )

    def parse_jobs(self,response):
        jobs_urls = set(response.xpath(self.config[response.meta.get('domain')]['xpaths']['jobs_urls']).getall()) if not self.config[response.meta.get('domain')] else \
            [response.urljoin(url) for url in response.xpath(self.config[response.meta.get('domain')]['xpaths']['jobs_urls']).getall()]
        for url in jobs_urls :
            yield Request(
                url,
                callback=self.parse_job,
                meta= {
                    'domain':response.meta.get('domain')
                }
            )

    def parse_job(self,response):
        domain = response.meta.get('domain')
        loader = ItemLoader(DetailsItem(),response)
        loader.add_value('job_url',response.url)
        loader.add_xpath('title',self.config[domain]['xpaths']['title']) if self.config[domain]['xpaths']['title'] else None 
        loader.add_xpath('work_place',self.config[domain]['xpaths']['work_place']) if self.config[domain]['xpaths']['work_place'] else None 
        loader.add_xpath('expiration_date',self.config[domain]['xpaths']['expiration_date']) if self.config[domain]['xpaths']['expiration_date'] else None 
        loader.add_xpath('applicant_level',self.config[domain]['xpaths']['applicant_level']) if self.config[domain]['xpaths']['applicant_level'] else None 
        loader.add_xpath('section',self.config[domain]['xpaths']['section']) if self.config[domain]['xpaths']['section'] else None 
        loader.add_xpath('number_of_available_jobs',self.config[domain]['xpaths']['number_of_available_jobs']) if self.config[domain]['xpaths']['number_of_available_jobs'] else None 
        loader.add_xpath('contracts_type',self.config[domain]['xpaths']['contracts_type']) if self.config[domain]['xpaths']['contracts_type'] else None 
        loader.add_xpath('description',self.config[domain]['xpaths']['description']) if self.config[domain]['xpaths']['description'] else None 
        yield loader.load_item()


if __name__ == '__main__':
    keyword = input('what keyword you want to choose in your search : ').strip()
    process = CrawlerProcess(
        {
            'FEED_URI':'output.csv',
            'FEED_FORMAT':'csv',
            #'LOG_LEVEL':'ERROR',
            'HTTPCACHE_ENABLED' : True,
            'USER_AGENT':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
        }
    )



    process.crawl(InfosSpider,keyword)
    process.start()
