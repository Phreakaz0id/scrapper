import os
import re
import scrapy
import time

from ..driver_utils import set_driver
from ..items import YaguarItem

from datetime import datetime
from logzero import logger, logfile

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType

LOGS_PATH = 'logs'
logfile_prefix = datetime.now().strftime("%m-%d-%Y")

# Categoria de Limpieza
CLEANING_DATA = {
    'CAT_LINK': 'refDepto3',
    'CATEGORIES': [
        ('ACCESORIOS DE LIMPIEZA', '9'),
        ('ADITIVOS PARA LA ROPA', '8'),
        ('ALCOHOL QUEMAR', '22'),
        ('APRESTOS', '6'),
        ('CERAS', '11'),
        ('DESODORANTES DE AMBIENTE', '29'),
        ('DESTAPA CAÑERIAS', '30'),
        ('DETERGENTES Y LAVAVAJILLAS', '3'),
        ('INSECTICIDAS', '13'),
        ('JABON PARA LA ROPA', '1'),
        ('LAVANDINA', '4'),
        ('LIMPIADORES', '5'),
        ('LIMPIADORES DE PISOS', '10'),
        ('LUSTRAMUEBLES', '33'),
        ('POMADA PARA CALZAD', '18'),
        ('ROL.COC/SERVILL', '2'),
        ('SUAVIZANTES', '12'),
    ]
}

# Categoria de Perfumeria
PERFUMERY_DATA = {
    'CAT_LINK': 'refDepto4',
    'CATEGORIES': [
        ('CERAS DEPILATORIAS', '34'),
        ('COLONIAS Y PERFUMES', '10'),
        ('CREMAS CORPORALES', '12'),
        ('CUIDADO CAPILAR', '14'),
        ('CUIDADO DENTAL', '8'),
        ('DESODORANTES PERSONALES', '11'),
        ('ESMALTES Y QUITAESMALTES', '29'),
        ('ESPONJAS DE BAÑO', '46'),
        ('FILOS PARA AFEITAR', '26'),
        ('GELES DE BAÑO', '13'),
        ('JABON TOCADOR', '19'),
        ('PAÑALES Y TOALLAS HUMEDAS', '5'),
        ('PAÑUELOS DESCAR', '28'),
        ('PRODUCTOS FARMACIA', '1'),
        ('PRODUCTOS PARA BEBES', '6'),
        ('PROTECCION FEMENINA', '16'),
        ('TALCOS/POLVOS', '9'),
        ('TINTURAS', '30'),
        ('TOALLAS DESMAQUILLANTES', '18')
    ]
}

CODE_X_PATH = '/html/body/table/tbody/tr[3]/td/table/tbody/tr[{row}]/td/table/tbody/tr/td[1]/table/tbody/tr/td[2]/p'

ELEMENTS_PER_PAGE = list(range(1, 40, 2))


class YaguarSpider(scrapy.Spider):
    name = 'yaguar'
    allowed_domains = ['https://shop.yaguar.com.ar/frontendSP/asp/home.asp#']
    start_urls = ['https://shop.yaguar.com.ar/frontendSP/asp/home.asp#/']
    driver = None
    custom_settings = {
        'FEED_EXPORT_FIELDS': [
            "category",
            "code",
            "product_name",
            "price"
        ]
    }

    def __init__(self, category):
        # Initializing log file
        logfile(f"{LOGS_PATH}/{logfile_prefix}_{self.name}.log", maxBytes=1e6, backupCount=3)

        self.category = category
        self.categories = self.get_subcategories_by_category(category)

        self.username = os.environ["YAGUAR_USERNAME"]
        self.password = os.environ["YAGUAR_PASSWORD"]
        super().__init__()

    def start_requests(self):
        self.login()
        url = 'https://shop.yaguar.com.ar/frontendSP/asp/home.asp#/'
        yield scrapy.Request(url=url, callback=self.parse)

    def set_driver(self):
        self.driver = set_driver()

    def login(self):
        # Use headless option to not open a new browser window
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless")
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

        self._log("👋 Requesting log in url...")
        self.driver.get('https://shop.yaguar.com.ar/frontendSP/asp/home.asp#/')

        USERNAME_INPUT = '/html/body/div/div[3]/div[1]/div[2]/form/fieldset/p[1]/input'
        PASSWORD_INPUT = '/html/body/div/div[3]/div[1]/div[2]/form/fieldset/p[2]/input[1]'
        LOGIN_BUTTON = '/html/body/div/div[3]/div[1]/div[2]/form/fieldset/p[2]/input[2]'

        self._log("👋 Ready to log in...")
        # Wait for page to load
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, USERNAME_INPUT))
        )

        username_input = self.driver.find_element(By.XPATH, USERNAME_INPUT)
        username_input.send_keys(self.username)

        password_input = self.driver.find_element(By.XPATH, PASSWORD_INPUT)
        password_input.send_keys(self.password)

        login_button = self.driver.find_element(By.XPATH, LOGIN_BUTTON)
        login_button.click()

        self._log("👋✅ Succesfully logged in!")

    def parse(self, response):
        self._log(f"⏰ Scraping started at {time.strftime('%H:%M:%S')}")

        category_link_id = self.categories['CAT_LINK']
        cat_link = self.driver.find_element(By.ID, category_link_id)
        cat_link.click()

        CATEGORIES = self.categories['CATEGORIES']

        ref_depto = category_link_id.split('refDepto')[1]
        LINK_PATH_TEMPLATE = '//a[@href="javascript:CargarIframeContenido(\'iframe_ListadoDeProductos.asp?IdDepto={ref_depto}&IdCategoria={category_id}\');"]'.replace('{ref_depto}', ref_depto)
        for category_name, category_id in CATEGORIES:
            self._log(f"🕷 Start parsing the {category_name} category.")
            category_link = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, LINK_PATH_TEMPLATE.replace('{category_id}', category_id))))
            category_link.click()

            time.sleep(2)

            # Search the iframe
            iframe = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"ifrContenido\"]")))

            self._log("🧪 Switching from default context (main page) to iframe context (product list) to scan products...")
            self.driver.switch_to.frame(iframe)
            self._log("🧪 Inside iframe context (product list), ready to scan products.")

            pages_text = self.driver.find_element_by_class_name('tcceleste').text
            max_pages = self.get_page_from_pages_text(pages_text)

            products = []
            products = self.search_products_in_page(products)
            max_pages = max_pages - 1

            self._log(f"🕷 {max_pages} pages remainig for {category_name} category.")

            while max_pages != 0:
                try:
                    next_page = self.driver.find_element_by_xpath("//*[contains(text(),'siguiente')]")
                    next_page.click()
                except NoSuchElementException:
                    self._log(f"🕷 No more pages for {category_name} category. Switching category.")

                products = self.search_products_in_page(products)
                max_pages = max_pages - 1

                self._log(f"🕷 {max_pages} pages remainig for {category_name} category.")

            products = list(set(products))

            self._log(f"📦 Ready to dump {len(products)} products data to csv items.")
            for product in products:
                item = self.create_item(category_name, product)
                yield item
            self._log(f"📦✅ Succesfully dumped {len(products)} products data to csv.")

            self._log("🧪 Switching from iframe context (product list) to default context (main page) to browse categories...")
            self.driver.switch_to.default_content()
            self._log("🧪 Back to default context (main page).")

        time.sleep(3)
        self.driver.stop_client()
        self.driver.close()

        self._log("🎉 Scrapping finished succesfully.")

    def create_item(self, category_name, product):
        code = product[0]
        product_name = product[1]
        product_price = product[2]

        item = YaguarItem()
        item["category"] = category_name
        item["code"] = code.replace(" ", "")
        item["product_name"] = product_name
        item["price"] = product_price

        return item

    def search_products_in_page(self, _products):
        PRODUCT_ROWS_CONTAINER_XPATH = "/html/body/table/tbody/tr[3]/td/table/tbody"
        product_rows_container = self.driver.find_element_by_xpath(PRODUCT_ROWS_CONTAINER_XPATH)
        product_rows = product_rows_container.find_elements_by_tag_name('tr')

        products = _products
        for product_row in product_rows:
            try:
                code = product_row.find_element_by_class_name('Bulto')

                product_name_container = product_row.find_element_by_class_name('SFPRODTITULOB')
                product_name_link = product_name_container.find_element_by_tag_name('a')
                product_name = product_name_link.text

                price_element = product_row.find_element_by_class_name('sfPRODPRECIOA')

                products.append((code.text, product_name, price_element.text))
            except NoSuchElementException:
                pass

        return products

    def get_page_from_pages_text(self, pages_text):
        return int(re.search(r'Página 1 de (.*?) ', pages_text).group(1))

    def get_subcategories_by_category(self, category):
        if category == "perfumeria":
            return PERFUMERY_DATA
        else:
            return CLEANING_DATA

    def _log(self, message):
        prefix = f"[{self.name}:{self.category}]"
        logger.info(prefix + " " + message)
