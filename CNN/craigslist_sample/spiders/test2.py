import csv
import scrapy
import re
import os.path
import csv
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from craigslist_sample.items import CNNItem


class MySpider(CrawlSpider):
    name = "cnn"
    allowed_domains = ["cnn.com"]
    start_urls = [url.strip() for url in open('items.csv').readlines()]

    rules = (
        Rule(SgmlLinkExtractor(allow=('http://www.cnn.com/\d{4}\/\d{2}\/\d{2}\/.*\/.*\/')), callback="parse_items", follow= True),
    )

    def parse_items(self, response):
        hxs = HtmlXPathSelector(response)
        items = []
        item = CNNItem()
        item["title"] = hxs.select('//h1[@class="pg-headline"]/text()').extract()
        item["article"] = hxs.select('//div[@class="zn-body__paragraph"]/text()').extract()
        item["link"] = response.url
        items.append(item)
        splitUrl = response.url.split('/')
        year = splitUrl[3]
        month = splitUrl[4]
        day = splitUrl[5]
        name1 = item["title"][0]
        name = "".join(re.findall("[a-zA-Z]+", name1))
        article = "\n".join(item['article'])
        save_path = os.path.join('data',year+"-"+month+"-"+day,name+".txt")
        if not os.path.exists(os.path.dirname(save_path)):
            try:
                os.makedirs(os.path.dirname(save_path))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        with open(save_path, 'a+') as f:
            f.write('name: {0} \nlink: {1}\n\n {2}'.format(name, item['link'], article.encode('utf8')))
        return(items)
