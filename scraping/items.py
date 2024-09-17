# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Inmueble(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    currency = scrapy.Field()
    location = scrapy.Field()
    characteristics = scrapy.Field()
    extras = scrapy.Field()
    description = scrapy.Field()
    url = scrapy.Field()