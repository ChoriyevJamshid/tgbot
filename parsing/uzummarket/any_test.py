from selenium import webdriver
import time

url = f'https://uzum.uz'

browser = webdriver.Chrome()
browser.get(url)
time.sleep(10)
