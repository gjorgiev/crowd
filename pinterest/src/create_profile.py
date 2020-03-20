from typing import Any
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import random
import string
import time
import names
import pickle
import os

def randomString(stringLength=4):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def setupChrome():
    PROXIES = ["207.229.93.68:1027","207.229.93.68:1028","207.229.93.68:1025","207.229.93.68:1029","207.229.93.68:1026"]
    PROXY = random.choice(PROXIES) # IP:PORT or HOST:PORT

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--proxy-server=%s' % PROXY)

    chrome = webdriver.Chrome(options=chrome_options)
    #chrome.get("http://whatismyipaddress.com")
    #time.sleep(1)
    chrome.implicitly_wait(30)
    return chrome
def createAccount():
    # Create browser object
    browser = setupChrome()
    try:
        browser.get('http://www.pinterest.com/')
        assert 'Pinterest' in browser.title
    except:
        browser.quit() 
        return None
    else:
    # click on sign up button
        try:
            browser.find_element_by_xpath("//div[@data-test-id='simple-signup-button']")
        except:
            signup=browser.find_element_by_xpath("//button[@data-test-id='simple-signup-button']")
        else:
            signup=browser.find_element_by_xpath("//div[@data-test-id='simple-signup-button']")
        signup.click()
        # Find all the elements from the page
        try:
            browser.find_element_by_id('email')
        except:
            browser.quit() 
            return None
        else:
            email = browser.find_element_by_id('email')
            password = browser.find_element_by_id('password')
            submit = browser.find_element_by_xpath("//button[@type='submit']")
            # Prepare the data to send in fields
            email_value = randomString() + "@hotmail.com"
            password_value = "password1234"
            # Send the data to fields
            email.send_keys(email_value)
            password.send_keys(password_value)
            time.sleep(5)
            try:
                browser.find_element_by_id('age')
            except:
                browser.quit() 
                return None
            else:
                age = browser.find_element_by_id('age')
                age_value = random.randint(23,50)
                age.send_keys(age_value)
                submit.click()
                try:
                    browser.find_element_by_xpath("//div[@data-test-id='nux_name_done_btn']")
                except:
                    browser.quit() 
                    return None
                else:
                    next = browser.find_element_by_xpath("//div[@data-test-id='nux_name_done_btn']")
                    next.click()
                    try:
                        browser.find_element_by_id('female')
                    except:
                        browser.get('https://www.pinterest.com')
                        female = browser.find_element_by_id('female')
                        female.click()
                    else:
                        female = browser.find_element_by_id('female')
                        female.click()
                        try:
                            browser.find_element_by_xpath("//button[@type='submit']")
                        except:
                            browser.get('https://www.pinterest.com')
                            submit = browser.find_element_by_xpath("//button[@type='submit']")
                            submit.click()
                        else:
                            submit = browser.find_element_by_xpath("//button[@type='submit']")
                            submit.click()
                            try:
                                browser.find_elements_by_class_name("NuxInterest")
                            except:
                                browser.get('https://www.pinterest.com')
                                interests = browser.find_elements_by_class_name("NuxInterest")
                                interests[0].is_displayed()
                                interests[0].click()
                            else:
                                interests = browser.find_elements_by_class_name("NuxInterest")
                                try:
                                    interests[0].is_displayed()
                                except:
                                    browser.get('https://www.pinterest.com')
                                    time.sleep(10)
                                    interests = browser.find_elements_by_class_name("NuxInterest")
                                    interests[0].is_displayed()
                                    interests[0].click()
                                else:
                                    interests[0].click()
                                interests = browser.find_elements_by_class_name("NuxInterest")
                                if interests[1].is_displayed():
                                    interests[1].click()
                                interests = browser.find_elements_by_class_name("NuxInterest")
                                if interests[2].is_displayed():
                                    interests[2].click()
                                interests = browser.find_elements_by_class_name("NuxInterest")
                                if interests[3].is_displayed():
                                    interests[3].click()
                                interests = browser.find_elements_by_class_name("NuxInterest")
                                if interests[4].is_displayed():
                                    interests[4].click()
                                submit = browser.find_element_by_xpath("//button[@type='submit']")
                                submit.click()
                                    #name
                                browser.get('https://www.pinterest.com/settings/edit-profile')
                                try:
                                    browser.find_element_by_id('first_name')
                                except:
                                    browser.quit() 
                                    return None
                                else:
                                    firstname = browser.find_element_by_id('first_name')
                                    firstname_value = names.get_first_name(gender='female')
                                    firstname.clear()
                                    firstname.send_keys(firstname_value)
                                    lastname = browser.find_element_by_id('last_name')
                                    lastname_value = names.get_last_name()
                                    lastname.clear()
                                    lastname.send_keys(lastname_value)
                                    done = browser.find_element_by_xpath("//div[contains(text(), 'Done')]")
                                    done.click()
                                    path = "cookies"
                                    file_path = os.path.join(path, email_value)
                                    pickle.dump(browser.get_cookies(), open(file_path + '.pkl',"wb"))
                                    browser.quit()
                                    return email_value + ',' + email_value + ',' + password_value + ",,,"
for i in range (1000):
    account = createAccount()
    if account is not None:
        with open(r'C:\Users\PC\Desktop\instagramer\accounts.txt', 'a') as a_writer:
            a_writer.writelines('\n'+account)