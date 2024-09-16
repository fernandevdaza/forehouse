from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time

# Initialize Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--ignore-ssl-errors')
chrome_options.add_argument('--allow-insecure-localhost')

# Explicitly accept insecure certificates
chrome_options.set_capability("acceptInsecureCerts", True)

# Initialize WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Navigate to the target page
driver.get(
    "https://www.remax.bo/PublicListingList.aspx#mode=gallery&tt=261&cr=2&mpts=19420&pt=19420&cur=USD&sb=PriceIncreasing&page=1&sc=120&rl=2800&pm=50487&cll=8078771&lsgeo=2800,50487,8078771,0&sid=e1083e16-9f2d-4c67-bab4-45bdb9ec1b0a")

# Increase wait time
wait = WebDriverWait(driver, 20)

# Wait for page elements to load
time.sleep(5)  # Delay to allow the page to load fully

# Wait for the results container to load
try:
    menu_casas = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'results-container')))
    print(f"Menu casas: {menu_casas}")
except Exception as e:
    print(f"Error locating the results container: {e}")
    driver.quit()

# Initialize an empty list to store the house data
lista_casas = []

# Find all property price elements
try:
    gallery_containers = menu_casas.find_elements(By.CLASS_NAME, "gallery-item-container")

    # Iterate over each property found
    for casa in gallery_containers:
        casa_data = {}

        # Get price
        try:
            gallery_price_main = casa.find_element(By.CLASS_NAME, "gallery-price-main")
            proplist_price = gallery_price_main.find_element(By.CLASS_NAME, "proplist_price")
            precio = proplist_price.text.strip()
            casa_data['precio'] = precio

            # Get the link to the detailed property page
            link_precio = proplist_price.get_attribute('href')
            casa_data['link'] = link_precio
        except Exception as e:
            print(f"Error extracting price or link: {e}")
            continue

        # Get image
        try:
            gallery_photo = casa.find_element(By.CLASS_NAME, "gallery-photo")
            img = gallery_photo.find_element(By.TAG_NAME, "img")
            casa_data['imagen'] = img.get_attribute('src')
        except Exception as e:
            print(f"Error extracting image: {e}")

        # Get number of bedrooms, bathrooms, and size
        try:
            gallery_icons = casa.find_element(By.CLASS_NAME, "gallery-icons")
            icon_items = gallery_icons.find_elements(By.CLASS_NAME, "gallery-attr-item-value")
            if len(icon_items) >= 3:
                casa_data['dormitorios'] = icon_items[0].text.strip()
                casa_data['baños'] = icon_items[1].text.strip()
                casa_data['superficie'] = icon_items[2].text.strip()
        except Exception as e:
            print(f"Error extracting attributes: {e}")

        # Append the data to the list
        lista_casas.append(casa_data)

except Exception as e:
    print(f"Error while processing the properties: {e}")

# Quit the driver
driver.quit()

# Save the data to a JSON file
with open('casas_remax.json', 'w', encoding='utf-8') as f:
    json.dump(lista_casas, f, ensure_ascii=False, indent=4)

print("Datos guardados en 'casas_remax.json'")
