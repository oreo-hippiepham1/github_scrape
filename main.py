import selenium
from selenium import webdriver

driver = webdriver.Chrome()
driver.get('https://amazon.com')

driver.quit()

print('DONE')