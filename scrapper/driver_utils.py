import os

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
from selenium.webdriver.chrome.options import Options


def set_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument('--remote-debugging-port=9222')
    options.binary_location = os.environ.get("CHROME_DRIVER")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--headless")
    driver = webdriver.Chrome(
        ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install(),
        options=options
    )

    return driver
