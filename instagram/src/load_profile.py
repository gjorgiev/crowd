import sys
sys.path.append('.')

import pickle
import selenium.webdriver
from common.utils import setup_chrome_mobile

driver = setup_chrome_mobile()
driver.get("http://www.google.com")
cookies = pickle.load(open("instagram\\data\\cookies\\op4ppov_7@hotmail.com.pkl", "rb"))
for cookie in cookies:
    if 'expiry' in cookie:
        del cookie['expiry']
    driver.add_cookie(cookie)
driver.get("http://www.instagram.com")
