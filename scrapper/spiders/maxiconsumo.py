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

        # Terminate Session
        time.sleep(3)
        self.driver.stop_client()
        self.driver.close()
