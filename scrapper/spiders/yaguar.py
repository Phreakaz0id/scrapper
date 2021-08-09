import scrapy
import time
from logzero import logger, logfile
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

CLEANING_CATEGORIES = [
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


CODE_X_PATH = '/html/body/table/tbody/tr[3]/td/table/tbody/tr[{row}]/td/table/tbody/tr/td[1]/table/tbody/tr/td[2]/p'

ELEMENTS_PER_PAGE = list(range(1, 40, 2))


class YaguarSpider(scrapy.Spider):
    # Initializing log file
    logfile('scrapper_spider.log', maxBytes=16, backupCount=3)
    name = 'yaguar'
    allowed_domains = ['https://shop.yaguar.com.ar/frontendSP/asp/home.asp#']
    start_urls = ['https://shop.yaguar.com.ar/frontendSP/asp/home.asp#/']
    driver = None

    def start_requests(self):
        self.login()
        url = 'https://shop.yaguar.com.ar/frontendSP/asp/home.asp#/'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        logger.info(f"Scraping started at {time.strftime('%H:%M:%S')}")

        CLEANING_CAT_LINK = 'refDepto3'
        cleaning_cat_link = self.driver.find_element(By.ID, CLEANING_CAT_LINK)
        cleaning_cat_link.click()

        LINK_PATH_TEMPLATE = '//a[@href="javascript:CargarIframeContenido(\'iframe_ListadoDeProductos.asp?IdDepto=3&IdCategoria={category_id}\');"]'
        for category_name, category_id in CLEANING_CATEGORIES:
            # link_path = LINK_PATH_TEMPLATE.replace('<category_id>', category_id)
            # category_link = self.driver.find_element(By.XPATH, link_path)
            category_link = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, LINK_PATH_TEMPLATE.replace('{category_id}', category_id))))
            category_link.click()

            time.sleep(1)

            # Search the iframe
            iframe = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"ifrContenido\"]")))

            PRODUCT_ROWS_CONTAINER_XPATH = "/html/body/table/tbody/tr[3]/td/table/tbody"

            # Try to switch to iframe
            self.driver.switch_to_frame(iframe)
            # Try to find product rows
            r = self.driver.find_element_by_xpath(PRODUCT_ROWS_CONTAINER_XPATH)

            print("///////////////")
            print(r)

            product_rows_container = self.driver.find_element_by_xpath(PRODUCT_ROWS_CONTAINER_XPATH)
            print(product_rows_container)

            # for i in ELEMENTS_PER_PAGE:
            #     wait = WebDriverWait(self.driver, 10)
            #     code = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/table/tbody/tr[3]/td/table/tbody/tr[1]/td/table/tbody/tr/td[1]/table/tbody/tr/td[2]/p')))

            #     print("///////////////////////////")
            #     # print(code)

        time.sleep(3)
        self.driver.stop_client()
        self.driver.close()

    def login(self):

        # Use headless option to not open a new browser window
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless")
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

        self.driver.get('https://shop.yaguar.com.ar/frontendSP/asp/home.asp#/')

        USERNAME_INPUT = '/html/body/div/div[3]/div[1]/div[2]/form/fieldset/p[1]/input'
        PASSWORD_INPUT = '/html/body/div/div[3]/div[1]/div[2]/form/fieldset/p[2]/input[1]'
        LOGIN_BUTTON = '/html/body/div/div[3]/div[1]/div[2]/form/fieldset/p[2]/input[2]'

        # Wait for page to load
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, USERNAME_INPUT))
        )

        username_input = self.driver.find_element(By.XPATH, USERNAME_INPUT)
        username_input.send_keys('Javierysurieta@gmail.com')

        password_input = self.driver.find_element(By.XPATH, PASSWORD_INPUT)
        password_input.send_keys('23173480059')

        login_button = self.driver.find_element(By.XPATH, LOGIN_BUTTON)
        login_button.click()
