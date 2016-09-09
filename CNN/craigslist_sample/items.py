from scrapy.item import Item, Field

class CNNItem(Item):
    title = Field()
    link = Field()
    article = Field()
