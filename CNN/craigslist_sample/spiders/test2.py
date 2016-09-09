from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from craigslist_sample.items import CNNItem


class MySpider(CrawlSpider):
    name = "cnn"
    allowed_domains = ["cnn.com"]
    start_urls = ["http://www.cnn.com/"]

    rules = (
        Rule(SgmlLinkExtractor(allow=('http://www.cnn.com/\d{4}\/\d{2}\/\d{2}\/.*\/.*\/')), callback="parse_items", follow= True),
    )

    def parse_items(self, response):
        hxs = HtmlXPathSelector(response)
        items = []
        item = CNNItem()
        item["title"] = hxs.select('//title/text()').extract()
        item["article"] = hxs.select('//div[@class="zn-body__paragraph"]/text()').extract()
        item["link"] = response.url
        items.append(item)
        return(items)
