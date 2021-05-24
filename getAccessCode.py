from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from pathlib import Path
import subprocess
from datetime import datetime

import platform

def get_all_plz(all_plz=False):
    """
    Set all_plz to True if you need to read all PLZ in (when you just started to look), 
    False if the myPlz.txt was created already by the program in a previous run through
    """
    file = 'myPlz.txt' if not all_plz else 'allPlz.txt'
    plz = list()
    with open('data/' + file) as f:
        plz = f.read().splitlines()
    return plz

# check if myPlz.txt already exists
try:
    ALL_PLZ = get_all_plz()
except:
    ALL_PLZ = get_all_plz(all_plz=True)

# these are part of the url, 
# if there are waiting rooms, you can go through them to find one that is available
SUBSERVERS_LESS = ['001', '005', '002']
SUBSERVES_MORE = ['001', '005', '002', '003', '229', '356', '357']

# enter user data or read from file
# Read user data from myData.txt if it exists
# File Format (cf. myDataDummie.txt): 
#       first line: email-adress
#       second line: phone number without leading 0
#       third line: age 
#       fourth line: path/to/script
#######################
user_data_p = Path('data/myData.txt')
if user_data_p.exists():
    with open(user_data_p, "r") as f:
        user_data = f.read().splitlines()
        EMAIL = user_data[0]
        TEL = user_data[1]
        AGE = user_data[2]
        try:
            if user_data[3] != '':
                SCRIPT = Path(user_data[3])
                if not SCRIPT.exists():
                    SCRIPT = None
            else:
                SCRIPT = None
        except:
            SCRIPT = None
else:
    EMAIL = input('Enter email: ')
    TEL = input('Enter phone (no spaces, without leading 0): ')
    AGE = input('Enter age: ')
    SCRIPT = input('Enter path to shell script to be executed every 3 minutes (leave blank, if there is none): ')
    user_data = [EMAIL, TEL, AGE, SCRIPT]
    with open(user_data_p, "w") as f:
        f.writelines([d+"\n" for d in user_data])
        

# These are used to check if you where able to get a code
# and updated to plz that still need to be checked
SUCCESS_PLZ = []

# I only use it on MacOS and Linux
SYSTEM = "linux" if platform.system() == 'Linux' else 'macOS'


repeat = True
start_time = datetime.now()
while repeat:
    with webdriver.Chrome(executable_path='./' + SYSTEM + '/chromedriver') as driver:   
        for plz in ALL_PLZ:

            if SCRIPT is not None:
                if (datetime.now() - start_time).seconds/60 > 3:
                    subprocess.run(['sh', str(SCRIPT)])
                    start_time = datetime.now()
            
            success = False
            for subserver in SUBSERVERS_LESS:
                if success:
                    break
                
                driver.get("https://" + subserver + "-iz.impfterminservice.de/impftermine/service?plz=" + plz)
                try:

                    # try to click the cookie button
                    try:
                        cookie_btn = WebDriverWait(driver, 2).until(presence_of_element_located((By.CSS_SELECTOR,'app-root > div > div > div > div:nth-child(2) a')))
                        cookie_btn.click()
                    except:
                        pass
                    # click the no button
                    no_btn = WebDriverWait(driver, 2).until(presence_of_element_located((By.CSS_SELECTOR, '.ets-radio-wrapper > label:last-child')))
                    no_btn.click()
                    loginForm = driver.find_element_by_css_selector('.ets-login-form-section-wrapper > div:last-child')

                    # enter your age and check
                    form_yes_btn = WebDriverWait(driver, 5).until(presence_of_element_located((By.CSS_SELECTOR,'form .ets-radio-control:first-child')))
                    form_yes_btn.click()
                    
                    age_input = driver.find_element_by_css_selector('form .form-control')
                    age_input.send_keys(AGE)
                    check_btn = driver.find_element_by_css_selector('form > div:last-child > button')
                    check_btn.click()
        
                    # enter email and phone number and submit
                    email_input = WebDriverWait(driver,5).until(presence_of_element_located((By.CSS_SELECTOR,'app-its-check-success form > div:first-child input')))
                    email_input.send_keys(EMAIL)
                    tel_input = driver.find_element_by_css_selector('app-its-check-success form > div:nth-child(2) input')
                    tel_input.send_keys(TEL)
                    #input('continue?')
                    get_code_btn = driver.find_element_by_css_selector('app-its-check-success form > div:nth-child(3) button')
                    get_code_btn.click()

                    # enter codes (needs to be done manually)
                    user_code = input("Enter code: ")
                    code_input = WebDriverWait(driver, 5).until(presence_of_element_located((By.CSS_SELECTOR, 'app-its-check-success form * label > input')))
                    code_input.send_keys(user_code)
                    submit_btn = driver.find_element_by_css_selector('app-its-check-success button')
                    submit_btn.click()
                    success = True
                    SUCCESS_PLZ.append(plz)
                except:
                    pass
    
    # remove all plz that where successfull
    for plz in ALL_PLZ:
        if plz in SUCCESS_PLZ:
            ALL_PLZ.remove(plz)
            print('removed ' + plz)
    
    with open('data/myPlz.txt', 'w') as f:
        for plz in ALL_PLZ:
            f.write(plz + '\n')
    
    repeat = True if input('Repeat? (y/n): ') == "y" else False
        
