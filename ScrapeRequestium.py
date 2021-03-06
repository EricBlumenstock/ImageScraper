import selenium.webdriver as webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities as DC
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as WDW
import urllib.request as urllib
from selenium.webdriver.common.by import By
import os, sys
from requestium import Session, Keys
import time

# Names files 0.png, 1.png, ...
def download_images(imgs: [], path: str, c=0):

    for i in imgs:
        urllib.urlretrieve(i, os.path.join(path, str(c) + '.png'))
        c = c+1

    urllib.urlcleanup()


# Converts a list containing elements to a list containing the elements' specified attribute
def to_attribute_list(elements: [], attribute: str) -> list():

    attributes = []

    for i in elements:
        attributes.append(i.get_attribute(attribute))

    return attributes


# Names directories 0, 1, 2, ... inside of a named directory if given or current directory by default
def create_directory(num=0, curdir='./') -> str:

    joined = os.path.join(curdir, str(num))

    if not os.path.exists(curdir):
        os.makedirs(curdir)

    while os.path.exists(joined):
        num = num + 1
        joined = os.path.join(curdir, str(num))

    os.makedirs(joined)

    return joined

def main():
    try:
        start = sys.argv[1]
    except:
        print('ERROR: Requires URL as the first argument.')
        quit(0)

    # Constants
    ALLDROPDOWN = '//*[@id="selectReadType"]/option[2]'
    ACTUALIMAGES = '//*[@id="divImage"]//img'
    IMGGROUPS = '.listing a'
    TITLE = '.bigChar'
    NEXT = '//*[(@id = "btnNext")]//src'

    s = Session(webdriver_path='C:\\Webdrivers\\chromedriver', browser='chrome')  # ,webdriver_options={'arguments': ['headless', 'disable-gpu']}

    s.driver.get(start)
    s.driver.ensure_element_by_css_selector(TITLE)
    title = s.driver.find_element_by_css_selector(TITLE).text
    groups = s.driver.find_elements_by_css_selector(IMGGROUPS)
    s.transfer_driver_cookies_to_session()
    begin = to_attribute_list(groups, 'href').pop()
    response = s.get(begin).xpath(ACTUALIMAGES)
    print(response)
    s.close()
    quit(2)
    # for g in reversed(groups):
    #     s.driver.execute_script('''window.open("''' + g + '''","_blank");''')  # open a new tab
    #     wait.until(EC.number_of_windows_to_be(2))
    #     wd.switch_to.window(wd.window_handles[1])
    #
    #     wait.until(EC.presence_of_element_located((By.XPATH, ALLDROPDOWN)))
    #     wd.find_element_by_xpath(ALLDROPDOWN).click()
    #
    #     wait.until_not(EC.presence_of_element_located((By.CSS_SELECTOR, '#selectPage')))  # wait for javascript
    #
    #     wait.until(EC.presence_of_all_elements_located((By.XPATH, ACTUALIMAGES)))
    #     imgs = wd.find_elements_by_xpath(ACTUALIMAGES)
    #
    #     wd.execute_script("window.stop();")  # stop loading the page
    #
    #     download_images(to_attribute_list(imgs, 'src'), create_directory(curdir=title))
    #
    #     wd.execute_script('''window.close();''')
    #     wd.switch_to.window(wd.window_handles[0])
    #
    #     print(str(groups.index(g)) + ' remaining out of ' + str(len(groups)))
    #
    # wd.quit()


main()
