import scrapy

class UltracasasSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'https://www.ultracasas.com/buscar/casa-en-venta--en--santa-cruz-de-la-sierra---santa-cruz?page=1',
    ]

    def parse(self, response):
        for quote in response.css('div.inmuebles-item'):
            yield {
                
            }

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
