import scrapy
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class MaxiconsumoSpider(scrapy.Spider):
    name = 'maxiconsumo'
    allowed_domains = ['https://maxiconsumo.com/sucursal_burzaco/']
    start_urls = ['https://maxiconsumo.com/sucursal_burzaco/']
    driver = None
    login_url = 'https://maxiconsumo.com/sucursal_burzaco/customer/account/login/'

    def start_requests(self):
        self.login()
        url = 'https://maxiconsumo.com/sucursal_burzaco/'
        yield scrapy.Request(url=url, callback=self.parse)

    def login(self):
        options = webdriver.ChromeOptions()
        # options.add_argument("start-maximized")
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        self.driver.get(self.login_url)

        wait = WebDriverWait(self.driver, 5)
        user_input = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="email"]')))
        user_input.send_keys('***REMOVED***')

        password_input = self.driver.find_element(By.XPATH, '//*[@id="pass"]')
        password_input.send_keys('***REMOVED***')

        enter_button = self.driver.find_element(By.XPATH, '//*[@id="send2"]')
        enter_button.click()

    def parse(self, response):
        urls = self.generate_paged_urls('https://maxiconsumo.com/sucursal_burzaco/limpieza.html?p={p}&product_list_limit=96', 14)

        for url in urls:
            self.driver.get(url)
            wait = WebDriverWait(self.driver, 5)
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="page-title-heading"]/span')))

            products_list = self.driver.find_elements_by_class_name('list-item')
            for product in products_list:
                product_element = product.find_element_by_class_name('product-item-link')
                product_name = product_element.text
                # product_href = product_element.get_attribute('href')
                prices = self.search_and_extract_product_price(product)
                print(product_name)
                print(prices)

        # Terminate Session
        time.sleep(3)
        self.driver.stop_client()
        self.driver.close()

    def generate_paged_urls(self, base_url, max_pages_num: int):
        urls_list = []

        for num in range(1, max_pages_num + 1):
            url = base_url.replace("{p}", str(num))
            urls_list.append(url)
        return urls_list

    def print_line(self, product_name, price_label, price):
        print(f"{product_name} - {price_label} - {price}")

    def print_one_price(self, product_name, label, price):
        bulto = "Precio unitario por bulto cerrado"

        if label == bulto:
            self.print_line(product_name, label, price)
            self.print_line(product_name, "Precio unitario", "$0")
        else:
            self.print_line(product_name, "Precio unitario por bulto cerrado", "$0")
            self.print_line(product_name, label, price)

    def search_and_extract_product_price(self, product):
        product_prices = product.find_elements_by_class_name('price-box')
        bundle_price = "$0"
        unit_price = "$0"

        for product_price in product_prices:
            label = product_price.find_element_by_class_name('price-label').text
            price = product_price.find_element_by_class_name('price').text
            if label == "Precio unitario por bulto cerrado":
                bundle_price = price
            if label == "Precio unitario":
                unit_price = price
        return (bundle_price, unit_price)
