from selenium.webdriver.chrome.options import Options
from selenium import webdriver

options = Options()
options.add_argument('--no-sandbox')
options.add_argument("--headless")
options.add_argument('--disable-dev-shm-usage')
import time

url = f'https://uzum.uz'

browser = webdriver.Chrome(options=options)
browser.get(url)
time.sleep(10)
print("ALL WORKS OK!!!")
