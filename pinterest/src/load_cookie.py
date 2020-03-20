import sys
sys.path.append('.')
import pickle
import selenium.webdriver
from common.tools.utils import setup_chrome_mobile

driver = setup_chrome_mobile()
cookies = pickle.load(open("pinterest\\cookies\\aegk@hotmail.com.pkl", "rb"))
for cookie in cookies:
    if 'expiry' in cookie:
        del cookie['expiry']
    driver.add_cookie(cookie)
driver.get("https://www.pinterest.com/pin/588564245039579576/")