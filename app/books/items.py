# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookItem(scrapy.Item):
    name = scrapy.Field()
    availability = scrapy.Field()
    upc = scrapy.Field()
    price_excl_tax = scrapy.Field()
    tax = scrapy.Field()
