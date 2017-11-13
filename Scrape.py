import selenium.webdriver as webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities as DC
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as WDW
import urllib.request as urllib
from selenium.webdriver.common.by import By
import os
import time


#Names files 0.png, 1.png, ...
def download_images(imgs:[], path:str):
    c = 0
    for i in imgs:
        urllib.urlretrieve(i, os.path.join(path, str(c) + '.png'))
        c = c+1
    urllib.urlcleanup()

#Converts a list containing elements to a list containing the elements' specified attribute
def to_attribute_list(elements:[], attribute:str):
    attributes = []
    for i in elements:
        attributes.append(i.get_attribute(attribute))

    return attributes

#Names directories 0, 1, 2, ...
def create_directory():
    num = 0
    while os.path.exists('./' + str(num)):
        num = num + 1
    os.makedirs('./' + str(num))

    return ('./' + str(num))


def main():

    wdo = webdriver.ChromeOptions()
    wdo.add_extension('C:\Webdrivers\extension_1_14_18.crx')
    capa = DC.CHROME
    capa["pageLoadStrategy"] = "none"

    #prefs = {"profile.managed_default_content_settings.images": 2}
    #wdo.add_experimental_option("prefs", prefs)
    #https://clients2.google.com/service/update2/crx?response=redirect&prodversion=60&x=id%3Dcjpalhdlnbpafiamejdnhcphjbkeiagm%26uc
    wd = webdriver.Chrome(chrome_options=wdo)
    wait = WDW(wd, 20)

    wd.get("http://kissmanga.com/Manga/Superior-Cross")
    time.sleep(6) #wait a moment for javascript to give us access to website

    groups = wd.find_elements_by_css_selector('.listing a')

    # BEGIN THREAD
    groups.pop().click() #navigate to a group of pages with images

    ALLIMAGES = '//*[@id="selectReadType"]/option[2]'
    ACTUALIMAGES = '//*[@id="divImage"]//img'


    wait.until(EC.presence_of_element_located((By.XPATH, ALLIMAGES))) #click ASAP
    wd.find_element_by_xpath(ALLIMAGES).click() #click the ALL images selection

    time.sleep(2)#wait a moment for javascript to load

    wait.until(EC.presence_of_all_elements_located((By.XPATH, ACTUALIMAGES))) #find all ASAP
    imgs = wd.find_elements_by_xpath(ACTUALIMAGES)  # find all of the images we want

    wd.execute_script("window.stop();") #stop loading the page

    download_images(to_attribute_list(imgs, 'src'), create_directory())

    wd.quit() #Unfortunately this has to remain open for the session to work

    #if wd.find_element_by_xpath('//*[@id="containerRoot"]/div[4]/div[1]/div[2]/a/img').is_displayed():
        #wd.find_element_by_xpath('//*[@id="containerRoot"]/div[4]/div[1]/div[2]/a/img').click()


    #wd.find_element_by_xpath('//*[@id="selectReadType"]/option[2]').click()
    #img = wd.find_elements_by_xpath('//*[@id="divImage"]//img')


main()
