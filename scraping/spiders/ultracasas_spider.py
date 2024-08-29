import scrapy
from scraping.items import Inmueble
class UltracasasSpider(scrapy.Spider):
    name = "Ultracasas"
    start_urls = [
        'https://www.ultracasas.com/buscar/casa-en-venta--en--santa-cruz-de-la-sierra---santa-cruz?page=1',
    ]
    page_limit = 55
    current_page = 1

    def parse(self, response):
        for item in response.css('div.inmuebles-item'):
            type_property = item.css('div.count-fotos-container-list a::attr(type-property)').get()
            self.log('Type property: %s' % type_property)
            href = item.css('a.cursor-pointer::attr(href)').get()

            if type_property == 'INMUEBLE':
                yield response.follow(href, self.parse_inmueble)
            if type_property == 'PROYECTO':
                yield response.follow(href, self.parse_proyecto)

        # Navegar a la siguiente página si no se ha alcanzado el límite
        if self.current_page < self.page_limit:
            self.current_page += 1
            next_page = f'https://www.ultracasas.com/buscar/casa-en-venta--en--santa-cruz-de-la-sierra---santa-cruz?page={self.current_page}'
            yield response.follow(next_page, self.parse)

    def parse_inmueble(self, response):
        item = Inmueble()
        item['title'] = response.css('span[itemprop=streetAddress]::text').get(default='').replace('\n', '').replace(
            '\r', '').strip()
        item['price'] = response.css('meta[itemprop=price]::attr(content)').get(default='').replace('\n', '').replace(
            '\r', '').strip()
        item['currency'] = response.css('meta[itemprop=priceCurrency]::attr(content)').get(default='').replace('\n',
                                                                                                               '').replace(
            '\r', '').strip()
        item['location'] = {
            'address': response.css('span[itemprop=streetAddress]::text').get(default='').replace('\n', '').replace(
                '\r', '').strip(),
            'city': response.css('span[itemprop=addressLocality]::text').get(default='').replace('\n', '').replace('\r',
                                                                                                                   '').strip(),
            'state': response.css('span[itemprop=addressRegion]::text').get(default='').replace('\n', '').replace('\r',
                                                                                                                  '').strip(),
            'lat': response.css('div[itemprop=geo] meta[itemprop=latitude]::attr(content)').get(default='').replace(
                '\n', '').replace('\r', '').strip(),
            'lng': response.css('div[itemprop=geo] meta[itemprop=longitude]::attr(content)').get(default='').replace(
                '\n', '').replace('\r', '').strip(),
        }
        characteristics_text = response.css('div.titular h3::text').get(default='').replace('\n', '').replace('\r',
                                                                                                              '').strip()
        characteristics_parts = characteristics_text.split(' · ')
        item['characteristics'] = {}

        for part in characteristics_parts:
            part_lower = part.lower()
            try:
                if 'dormitorio' in part_lower:
                    item['characteristics']['bedrooms'] = int(part.split()[0])
                elif 'baño' in part_lower:
                    item['characteristics']['bathrooms'] = int(part.split()[0])
                elif 'garaje' in part_lower:
                    item['characteristics']['garages'] = int(part.split()[0])
                elif 'm' in part_lower:
                    area_value = part.replace(',', '').split()[0]
                    if area_value.replace('.', '', 1).isdigit():  # Verifica que sea un número antes de convertirlo
                        item['characteristics']['area'] = float(area_value)
            except (ValueError, IndexError):
                self.log(f"Error parsing characteristic part: {part}", level=scrapy.log.WARNING)

        extras = response.css('div.caracteristicas ul.list-inline li')
        item['extras'] = {}
        for extra in extras:
            key = extra.css('div.listado-features-texto h4::text').get(default='').replace('\n', '').replace('\r',
                                                                                                             '').strip()
            value = extra.css('div.listado-features-texto p::text').get(default='').replace('\n', '').replace('\r',
                                                                                                              '').strip()

            key = ' '.join(key.split())
            value = ' '.join(value.split())

            if value == "":
                item['extras'][key] = True
            else:
                item['extras'][key] = value

        item['description'] = response.css('div.parrafo p::text').get(default='').replace('\n', '').replace('\r',
                                                                                                            '').strip()
        item['url'] = response.url

        yield item

    def parse_proyecto(self, response):
        table = response.css('table.table tbody tr')
        for house in table:
            title = house.css('td:nth-of-type(2)::text').get().replace('\n', '').replace('\r', '').strip()
            if 'terreno' in title.lower():
                continue
            href = house.css('td a::attr(href)').get()
            yield response.follow(href, self.parse_inmueble)
