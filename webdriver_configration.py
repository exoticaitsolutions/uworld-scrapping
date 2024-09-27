from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from seleniumbase import Driver
import undetected_chromedriver as uc


def driver_confrigration():
    options = uc.ChromeOptions()
    options.add_argument("--disable-notifications")
    options.add_argument("--start-maximized")
    driver = uc.Chrome(options=options)
    return driver