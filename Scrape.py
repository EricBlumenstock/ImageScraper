import selenium.webdriver as webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities as DC
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as WDW
import urllib.request as urllib
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import os
import time
import timeit


#Names files 0.png, 1.png, ...
def download_images(imgs: [], path: str):
    c = 0
    for i in imgs:
        urllib.urlretrieve(i, os.path.join(path, str(c) + '.png'))
        c = c+1
    urllib.urlcleanup()


#Converts a list containing elements to a list containing the elements' specified attribute
def to_attribute_list(elements: [], attribute: str):
    attributes = []
    for i in elements:
        attributes.append(i.get_attribute(attribute))

    return attributes


#Names directories 0, 1, 2, ...
def create_directory(num=0):
    while os.path.exists('./' + str(num)):
        num = num + 1
    os.makedirs('./' + str(num))

    return './' + str(num)


def main():

    START = 'http://kissmanga.com/Manga/Superior-Cross'
    ALLDROPDOWN = '//*[@id="selectReadType"]/option[2]'
    ACTUALIMAGES = '//*[@id="divImage"]//img'
    IMGGROUPS = '.listing a'

    wdo = webdriver.ChromeOptions()
    wdo.add_extension('C:\Webdrivers\extension_1_14_18.crx')
    #wdo.add_argument('--headless')
    #wdo.add_argument('--disable-gpu')

    capa = DC.CHROME
    capa["pageLoadStrategy"] = "none"

    #prefs = {"profile.managed_default_content_settings.images": 2}
    #wdo.add_experimental_option("prefs", prefs)
    #https://clients2.google.com/service/update2/crx?response=redirect&prodversion=60&x=id%3Dcjpalhdlnbpafiamejdnhcphjbkeiagm%26uc
    wd = webdriver.Chrome(chrome_options=wdo)
    wait = WDW(wd, 20)

    start = timeit.default_timer()

    wd.get(START)
    time.sleep(6) #wait a moment for javascript to give us access to website

    groups = wd.find_elements_by_css_selector(IMGGROUPS)

    # BEGIN THREAD

    groups = to_attribute_list(groups, 'href')


    for g in reversed(groups):
        wd.execute_script('''window.open("''' + g + '''","_blank");''')
        time.sleep(1)
        wd.switch_to.window(wd.window_handles[1])

        wait.until(EC.presence_of_element_located((By.XPATH, ALLDROPDOWN))) #click ASAP
        wd.find_element_by_xpath(ALLDROPDOWN).click() #click the ALL images selection
        time.sleep(4)
        wait.until(EC.presence_of_all_elements_located((By.XPATH, ACTUALIMAGES))) #find all ASAP
        imgs = wd.find_elements_by_xpath(ACTUALIMAGES)  # find all of the images we want

        wd.execute_script("window.stop();") #stop loading the page

        #download_images(to_attribute_list(imgs, 'src'), create_directory())

        #Close tab
        wd.execute_script('''window.close();''')
        wd.switch_to.window(wd.window_handles[0])
        #body = wd.find_element(By.TAG_NAME, 'body')
        #body.send_keys(Keys.CONTROL, 'w')

    wd.quit() #Unfortunately this has to remain open for the session to work

    print(timeit.default_timer() - start)#12

main()
