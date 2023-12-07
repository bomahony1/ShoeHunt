# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class BookItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    product_type = scrapy.Field()
    price = scrapy.Field()
    availability = scrapy.Field()
    stars = scrapy.Field()


class NikeItem(scrapy.Item):
    title = scrapy.Field()
    category = scrapy.Field()
    original_price = scrapy.Field()
    discount_price = scrapy.Field()
    discount_percent = scrapy.Field()
    image_url = scrapy.Field()
    description = scrapy.Field()
    product_url = scrapy.Field()


class JDSportItem(scrapy.Item):
    title = scrapy.Field()
    category = scrapy.Field()
    original_price = scrapy.Field()
    discount_price = scrapy.Field()
    discount_percent = scrapy.Field()
    image_url = scrapy.Field()
    description = scrapy.Field()
    product_url = scrapy.Field()

    
  
