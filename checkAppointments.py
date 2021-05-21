from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located

import platform

PATHTOCODES = 'data/accessCodes.txt'

SUBSERVERS_LESS = ['001', '005', '002']
SUBSERVES_MORE = ['001', '005', '002', '003', '229', '356', '357']

# I only use it on MacOS and Linux
SYSTEM = "linux" if platform.system() == 'Linux' else 'macOS'

LINKS = list()

# creates the accesCodes.txt if not found
try:
    with open(PATHTOCODES) as f:
        LINKS = f.read().splitlines()
except:
    with open(PATHTOCODES, 'w') as f:
        pass

repeat = True
while repeat:

    with webdriver.Chrome(executable_path='./' + SYSTEM + '/chromedriver') as driver:   
        for link in LINKS:
            driver.get(link)
            # try to click the cookie button
            try:
                cookie_btn = WebDriverWait(driver, 2).until(presence_of_element_located((By.CSS_SELECTOR,'app-root > div > div > div > div:nth-child(2) a')))
                cookie_btn.click()
            except:
                pass
            # Termine Suchen Button
            try:
                search_btn = WebDriverWait(driver,5).until(presence_of_element_located((By.CSS_SELECTOR,'app-page-its-search button')))
                search_btn.click()
            except:
                continue
            # No appointments available field
            try:
                none_available_field = WebDriverWait(driver,5).until(presence_of_element_located((By.CSS_SELECTOR, 'app-its-search-slots-modal form .its-slot-pair-search-no-results')))
                none_available_field.text
            except:
                input('Check appointments, press enter when done')
    
    repeat = True if input('Repeat? (y/n): ') == "y" else False