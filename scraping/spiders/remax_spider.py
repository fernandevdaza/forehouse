import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.selector import Selector
import logging
from scraping.items import Inmueble
import re


class CasasRemaxSpider(scrapy.Spider):
    name = 'casas_remax'
    allowed_domains = ['remax.bo']
    start_urls = ["https://www.remax.bo/PublicListingList.aspx"]

    def __init__(self, *args, **kwargs):
        super(CasasRemaxSpider, self).__init__(*args, **kwargs)
        chrome_options = Options()
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--ignore-ssl-errors')
        chrome_options.add_argument('--allow-insecure-localhost')
        prefs = {"intl.accept_languages": "es-BO,es"}
        chrome_options.add_experimental_option("prefs", prefs)
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    def parse(self, response):
        url = "https://www.remax.bo/PublicListingList.aspx#mode=gallery&tt=261&cr=2&mpts=19420&pt=19420&cur=USD&sb=PriceIncreasing&page=1&sc=120&rl=2800&pm=50487&cll=8078771&lsgeo=2800,50487,8078771,0&sid=e1083e16-9f2d-4c67-bab4-45bdb9ec1b0a"

        # Navegar a la página inicial con Selenium
        self.driver.get(url)
        current_page = 1
        get_page = 19
        while current_page < get_page:
            try:
                next_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'li a.ajax-page-link i.page-next'))
                )

                if "disabled" in next_button.get_attribute("class"):
                    self.logger.debug("Botón 'Next' está deshabilitado. Fin de la paginación.")
                    break

                old_url = self.driver.current_url
                next_button.find_element(By.XPATH, '..').click()

                WebDriverWait(self.driver, 60).until(
                    lambda driver: driver.current_url != old_url
                )

                WebDriverWait(self.driver, 60).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div.gallery-item-container'))
                )

                current_page += 1

            except Exception as e:
                self.logger.debug(f"No se pudo pasar a la siguiente página: {str(e)}")
                break

        while True:
            self.logger.debug(f"Procesando la página {current_page}")

            try:
                WebDriverWait(self.driver, 60).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div.gallery-item-container'))
                )

                sel = Selector(text=self.driver.page_source)
                properties = sel.css(
                    '.gallery-item-container div.gallery-item div.gallery-price a::attr(href)').getall()

                for property_url in properties:
                    full_url = response.urljoin(property_url)
                    yield scrapy.Request(full_url, callback=self.parse_property)

                try:
                    next_button = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, 'li a.ajax-page-link i.page-next'))
                    )

                    if "disabled" in next_button.get_attribute("class"):
                        self.logger.debug("Botón 'Next' está deshabilitado. Fin de la paginación.")
                        break

                    old_url = self.driver.current_url
                    next_button.find_element(By.XPATH, '..').click()

                    WebDriverWait(self.driver, 60).until(
                        lambda driver: driver.current_url != old_url
                    )

                    WebDriverWait(self.driver, 60).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.gallery-item-container'))
                    )

                    current_page += 1

                except Exception as e:
                    self.logger.debug(f"No se pudo pasar a la siguiente página: {str(e)}")
                    break

            except Exception as e:
                self.logger.error(f"Error durante el procesamiento de la página: {str(e)}")
                break

    def parse_property(self, response):
        self.driver.get(response.url)

        WebDriverWait(self.driver, 35).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.col-xs-12.key-title'))
        )

        sel = Selector(text=self.driver.page_source)

        inmueble = Inmueble()

        inmueble['title'] = sel.css('div.col-xs-12.key-title h2.fts-mark::text').get().strip()
        inmueble['price'] = sel.css('div.col-xs-12.key-price a[itemprop="price"]::attr(content)').get().strip()
        inmueble['currency'] = sel.css(
            'div.col-xs-12.key-price span[itemprop="priceCurrency"]::attr(content)').get().strip()

        address = sel.css('div.col-xs-12.key-address::text').get()
        if address:
            address = address.strip()
        else:
            address = 'Dirección no disponible'
        if '-' in address:
            address_parts = address.split(' - ')
            street_info = ' - '.join(address_parts[:-1]) if len(address_parts) > 1 else address
            city_info = address_parts[-1] if len(address_parts) > 1 else ''
            city_parts = city_info.split(',')
        else:
            street_info = address
            city_info = address
            city_parts = city_info.split(',')

        lat_pattern = re.compile(r'var lat = (-?\d+\.\d+);')
        lng_pattern = re.compile(r'var lng = (-?\d+\.\d+);')

        lat = None
        lng = None

        script_content = sel.css('script::text').getall()
        for script in script_content:
            lat_match = lat_pattern.search(script)
            lng_match = lng_pattern.search(script)
            if lat_match and lng_match:
                lat = lat_match.group(1)
                lng = lng_match.group(1)
                break

        inmueble['location'] = {
            'address': street_info,
            'city': city_parts[0].strip() if len(city_parts) > 0 else 'Ciudad no disponible',
            'state': city_parts[-1].strip() if len(city_parts) > 1 else 'Estado no disponible',
            'lat': lat,
            'lng': lng,
        }

        characteristics = {
            'bedrooms': 0,
            'bathrooms': 0,
            'area': 0,
            'garages': 0
        }

        extras = {}

        first_row = sel.css('div.attributes-data-row').get()

        if first_row:
            first_row_selector = Selector(text=first_row)
            icons = first_row_selector.css('div.attributes-icons')
            for icon in icons:
                label = icon.css('div.data-item-label span::text').get()
                value = icon.css('div.data-item-value span::text').get()

                if label and value:
                    label = label.strip()
                    value = value.strip()

                    if "Dormitorios" in label:
                        characteristics['bedrooms'] = int(value)
                    elif "Baños" in label:
                        characteristics['bathrooms'] = int(value)
                    elif "Area" in label:
                        try:
                            characteristics['area'] = float(value.replace("m²", "").strip())
                        except ValueError:
                            characteristics['area'] = 0.0
                    elif "Terreno" in label:
                        try:
                            extras['Terreno'] = float(value.replace("m²", "").strip())
                        except ValueError:
                            extras['Terreno'] = 0.0
                    elif "Año" in label:
                        try:
                            extras['Año construcción'] = int(value.split("/")[0].strip())
                        except ValueError:
                            extras['Año construcción'] = 0
                    elif "Estacionamientos" in label or "Garages" in label:
                        characteristics['garages'] = int(value)

        inmueble['characteristics'] = characteristics

        extra_features = sel.css('div.features-container span.feature-item')
        for feature in extra_features:
            feature_name = feature.css('::text').get().strip()
            extras[feature_name] = True

        inmueble['extras'] = extras

        description = sel.css('div#ListingFullLeft_ctl01_DescriptionDivShort::text').getall()
        inmueble['description'] = ' '.join([text.strip() for text in description if text.strip()])
        inmueble['url'] = response.url

        yield inmueble

    def closed(self, reason):
        try:
            if self.driver:
                self.driver.quit()
        except Exception as e:
            self.logger.error(f"Error al cerrar Selenium: {str(e)}")
