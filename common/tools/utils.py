from selenium import webdriver
import time
import random
import os
import re
import pickle

def setup_chrome_mobile():
    PROXIES = ["207.229.93.68:1027","207.229.93.68:1028","207.229.93.68:1025","207.229.93.68:1029","207.229.93.68:1026"]
    PROXY = random.choice(PROXIES) # IP:PORT or HOST:PORT
    mobile_emulation = { "deviceName": "iPhone X" }
    prefs = {"profile.managed_default_content_settings.images": 2}

    options = webdriver.ChromeOptions()
    options.add_argument('--proxy-server=%s' % PROXY)
    options.add_argument("--disable-notifications")
    options.add_argument("--headless")
    options.add_experimental_option("mobileEmulation", mobile_emulation)
    options.add_experimental_option("prefs", prefs)

    #driver = webdriver.Remote(command_executor='http://127.0.0.1:4444/wd/hub', desired_capabilities = chrome_options.to_capabilities())
    driver = webdriver.Chrome(options=options)
    driver.get("http://google.com")
    # driver.get("https://www.whatismyip.com/")
    driver.implicitly_wait(5)
    print('Chrome mobile is being setup')
    return driver

def setup_chrome():
    PROXIES = ["207.229.93.68:1027","207.229.93.68:1028","207.229.93.68:1025","207.229.93.68:1029","207.229.93.68:1026"]
    PROXY = random.choice(PROXIES) # IP:PORT or HOST:PORT
    # prefs = {"profile.managed_default_content_settings.AnimatedImage": 2, "profile.managed_default_content_settings.images": 2}

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--proxy-server=%s' % PROXY)
    chrome_options.add_argument("--disable-notifications")
    # chrome_options.add_argument("--headless")
    # chrome_options.add_experimental_option("prefs", prefs)

    chrome = webdriver.Chrome(options=chrome_options)
    chrome.get("http://google.com")
    chrome.implicitly_wait(10)
    return chrome

def cookie_driver(name):
    driver = setup_chrome()
    # load cookies for account
    cookies = pickle.load(open(os.path.join('cookies', name), "rb"))
    for cookie in cookies:
        if 'expiry' in cookie:
            del cookie['expiry']
        driver.add_cookie(cookie)
    driver.implicitly_wait(10)
    return driver

def setup_chrome_mobile_cookie(cookies_path, name):
    driver = setup_chrome_mobile()
    # load cookies for account
    cookies = pickle.load(open(os.path.join(cookies_path, name), "rb"))
    for cookie in cookies:
        if 'expiry' in cookie:
            del cookie['expiry']
        driver.add_cookie(cookie)
    return driver


def save_line_to_file(filename, line):
    if os.path.exists(filename):
        append_write = 'a'
    else:
        append_write = 'w'
    writer = open(filename, append_write)
    writer.writelines(line)
    writer.close()

def remove_text_from_file(text, filename):
    with open(filename,"r+") as f:
        new_f = f.readlines()
        f.seek(0)
        for line in new_f:
            if text not in line or re.match(r'^\s*$', line):
                f.write(line)
        f.truncate()

def remove_newline(text):
    return text.replace('\n', '').replace('\t','').replace('\r','')

def read_file_as_array(path):
    array = []
    try:
        with open(path, 'r') as data:
            for line in data.readlines():
                array.append(line)
    except Exception:
        print (path + " not found")
    return array

def read_first_line(path):
    with open(path) as f:
        return f.readline()

def remove_first_line(path):
    with open(path, 'r') as fin:
        data = fin.read().splitlines(True)
    with open(path, 'w') as fout:
        fout.writelines(data[1:])

def read_random_line(path):
    with open(path) as f:
        lines = f.readlines()
        return random.choice(lines)