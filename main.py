import MSAccount
import WordManager

import threading






from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options 

import time
import random



WEB_DELAY= 8
DASHBOARD = "https://account.microsoft.com/rewards/"
BING = "https://www.bing.com"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.864.37"
MOBILE_USER_AGENT ="Mozilla/5.0 (iPhone; CPU iPhone OS 14_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
EXEC_PATH = "C:\\geckodriver\\geckodriver.exe"
DELAY_TYPE = 0.25

MSAccountMan= MSAccount.MSAccountManager()
if MSAccountMan.loadFile() == False:
    quit(1)
else:
    print("MSAccountManager has read all the accounts!")

WordMan = WordManager.WordManager()
if WordMan.loadFile() == False:
    quit(1)
else:
    print("WordManager has indexed the dictionary!")

MSAccounts= MSAccountMan.getAccounts()
words =  WordMan.getWords()

# MSAccountManager -> loadfile -> get password
# login -> open dashboard -> bing searches -> logout -> repeat

thread1= None
thread2 = None


print("Starting Firefox!")




profile = webdriver.FirefoxProfile()
profile.set_preference("general.useragent.override", USER_AGENT)

options = Options()
options.headless = True



driver = webdriver.Firefox(executable_path=EXEC_PATH, firefox_profile=profile, options=options)

mob_profile = webdriver.FirefoxProfile()
mob_profile.set_preference("general.useragent.override", MOBILE_USER_AGENT)
mob_driver =  webdriver.Firefox(executable_path=EXEC_PATH, firefox_profile=mob_profile, options=options)
linkFix = ''
def slowType(e, word, delay):
    for c in word:
        e.send_keys(c)
        time.sleep(delay)
    return

def login(num, MSAccount, whichDriver, mob):
    try:
        retry =0
        if mob == True:
            mob_driver.get(BING)
            time.sleep(WEB_DELAY)

            #if num == 0 and retry ==0:
            #    whichDriver.find_element_by_id("bnp_btn_accept").click()
            mob_driver.find_element_by_xpath('//*[@id="mHamburger"]').click()
            time.sleep(5)
            a= mob_driver.find_element_by_css_selector("#HBSignIn > a:nth-child(1)")
            mob_driver.get(a.get_attribute("href"))
        else:
            driver.get(BING)
            time.sleep(WEB_DELAY)
            #if num ==0 and retry ==0:
            #    whichDriver.find_element_by_id("bnp_btn_accept").click()
            signin= driver.find_element_by_xpath('//*[@id="id_l"]')
            signin.click()
            time.sleep(WEB_DELAY)    
        
        time.sleep(WEB_DELAY)
        email = whichDriver.find_element_by_id("i0116")
        slowType(email, MSAccount.getEmail(), DELAY_TYPE)
        emailSignIn = whichDriver.find_element_by_id("idSIButton9")
        emailSignIn.click()
        time.sleep(WEB_DELAY)
        password= whichDriver.find_element_by_xpath('//*[@id="i0118"]')
        slowType(password, MSAccount.getPassword(), DELAY_TYPE)
        time.sleep(2)
        passwordSignIn = whichDriver.find_element_by_xpath('//*[@id="idSIButton9"]')
        passwordSignIn.click()
        time.sleep(WEB_DELAY)
        return True
    except:
        retry = retry+1
        if mob == True:
            print("Trying again! Login! Mobile!")
            whichDriver.get_screenshot_as_file(f'screenshot_mob.png')
            login(num,MSAccount,whichDriver,mob)
        else:
            print("Trying again! Login! PC!")
            whichDriver.get_screenshot_as_file(f'screenshot.png')
            login(num, MSAccount, whichDriver,mob)


def logout(whichDriver):
    try:
        whichDriver.get(DASHBOARD)
        time.sleep(WEB_DELAY)
        whichDriver.find_element_by_id("mectrl_main_trigger").click()
        time.sleep(1)
        whichDriver.find_element_by_id("mectrl_body_signOut").click()
        time.sleep(WEB_DELAY)
        return
    except:
        print("Trying again! LOGOUT!")
        logout(whichDriver)






def search(whichDriver):
    try:
        keyword = words[random.randint(0, len(words))]
        searchBox=  whichDriver.find_element_by_id("sb_form_q")
        slowType(searchBox,keyword,DELAY_TYPE)
        searchBox.send_keys(Keys.ENTER)
        time.sleep(WEB_DELAY)
        
        clearTextBoxJs = 'box= document.getElementById("sb_form_q"); box.value = ""'
        whichDriver.execute_script(clearTextBoxJs)
        return
    except:
        print("Trying Again!")
        search(whichDriver)











    
    

def main():
    for num, msAccount in enumerate(MSAccounts):
        login(num, msAccount, driver, False)
        time.sleep(WEB_DELAY)
        #accept button thing manage cookies
        for _ in range(34):
            search(driver)
        logout(driver)
    
    driver.quit()

def MOB_main():
    for num, msAccount in enumerate(MSAccounts):
        login(num, msAccount,mob_driver, True)
        time.sleep(WEB_DELAY)
        #accept button thing manage cookies
        for _ in range(20):
            search(mob_driver)
        logout(mob_driver)
    mob_driver.quit()


thread1= threading.Thread(target=main)
thread2= threading.Thread(target=MOB_main)
thread1.start()
thread2.start()