import scrapy
from src.scraping.scraping.items import Inmueble
class UltracasasSpider(scrapy.Spider):
    name = "Ultracasas" 
    start_urls = [
        'https://www.ultracasas.com/buscar/casa-en-venta--en--santa-cruz-de-la-sierra---santa-cruz?page=1',
    ]

    def parse(self, response):
        for item in response.css('div.inmuebles-item'):
            type_property = item.css('a.fas::atr(type-property)').get()

            href = item.css('.cursor-pointer::attr(href)').get()

            if type_property == 'INMUEBLE':
                yield response.follow(href, self.parse_inmueble)
            if type_property == 'PROYECTO':
                yield response.follow(href, self.parse_proyecto)

    def parse_inmueble(self, response):
        item = Inmueble()
        item['title'] = response.css('meta[itemprop=name]::attr(content)').get()
        item['price'] = response.css('meta[itemprop=price]::attr(content)').get()
        item['currency'] = response.css('meta[itemprop=priceCurrency]::attr(content)').get()
        item['location'] = {
            'address': response.css('div.titular h1[itemprop=streetAddress]').get(),
            'lat': response.css('div[itemprop=geo] meta[itemprop=latitude]::attr(content)').get(),
            'lng': response.css('div[itemprop=geo] meta[itemprop=longitude]::attr(content)').get(),
        }
        characteristics_text = response.css('div.titular h3::text').get()
        characteristics_parts = characteristics_text.split(' · ')
        item['characteristics'] = {}
        for part in characteristics_parts:
            part_lower = part.lower()
            if 'dormitorio' in part_lower:
                item['characteristics']['bedrooms'] = int(part.split()[0])
            elif 'baño' in part_lower:
                item['characteristics']['bathrooms'] = int(part.split()[0])
            elif 'garaje' in part_lower:
                item['characteristics']['garages'] = int(part.split()[0])
            elif 'm' in part_lower and '2' in part_lower:
                item['characteristics']['area'] = float(part.split()[0])
        item['description'] = response.css('div.parrafo p::text').get()

        yield item
    def parse_proyecto(self, response):
        pass
