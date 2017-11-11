import selenium.webdriver as webdriver
import selenium.webdriver.support.ui as ui
import urllib.request as urllib


def main():

    wd = webdriver.Chrome()

    wd.get("http://kissmanga.com/Manga/Superior-Cross/Vol-001-Ch-001-Read-Online?id=123252#1")
    wd.find_element_by_xpath('//*[@id="selectReadType"]/option[2]').click()
    img = wd.find_elements_by_xpath('//*[@id="divImage"]//img[@src]')
    wd.close()

    for i in img:
        urllib.urlretrieve(img, i + '.png')

    urllib.urlcleanup()


main()
