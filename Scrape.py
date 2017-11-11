import selenium.webdriver as webdriver
import selenium.webdriver.support.ui as ui
import urllib.request as urllib
import time

def main():

    wdo = webdriver.ChromeOptions()
    #prefs = {"profile.managed_default_content_settings.images": 2}
    #wdo.add_experimental_option("prefs", prefs)
    #https://clients2.google.com/service/update2/crx?response=redirect&prodversion=60&x=id%3Dcjpalhdlnbpafiamejdnhcphjbkeiagm%26uc
    wdo.add_extension('C:\Webdrivers\extension_1_14_18.crx')

    wd = webdriver.Chrome(chrome_options = wdo)

    wd.implicitly_wait(5)
    wd.get("http://kissmanga.com/Manga/Superior-Cross/Vol-001-Ch-001-Read-Online?id=123252#1")
    wd.find_element_by_xpath('//*[@id="selectReadType"]/option[2]').click()
    img = wd.find_elements_by_xpath('//*[@id="divImage"]//img')

    c=0
    for i in img:
        urllib.urlretrieve(i.get_attribute('src'), str(c) + '.png')
        c=c+1
    wd.close()
    urllib.urlcleanup()


main()
