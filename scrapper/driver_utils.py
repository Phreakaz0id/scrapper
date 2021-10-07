import os

from logzero import logger
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType


def set_driver():
    logger.info("[Driver Utils] 🛠 Setting Driver...")
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-extensions')
    # options.add_argument('--no-sandbox')
    options.add_argument('--remote-debugging-port=9222')
    chrome_driver = os.environ.get("BROWSER_BINARY")
    logger.info(f"[Driver Utils] 🛠 BROWSER_BINARY: {chrome_driver}")
    if chrome_driver is None:
        raise Exception("BROWSER_BINARY env is not defined")
    options.binary_location = chrome_driver
    # options.add_argument("--headless")

    executable_path = os.environ.get("DRIVER_EXECUTABLE_PATH")
    driver = None
    if executable_path is None:
        logger.info("[Driver Utils] 🛠 DRIVER MANAGER: using manager from cache.")
        driver = webdriver.Chrome(
            ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install(),
            options=options
        )
    else:
        logger.info(f"[Driver Utils] 🛠 DRIVER MANAGER: using executable_path='{executable_path}'.")
        driver = webdriver.Chrome(
            executable_path=executable_path, options=options
        )

    return driver
