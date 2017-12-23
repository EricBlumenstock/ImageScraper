import selenium.webdriver as webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities as DC
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait as WDW
import urllib.request as urllib
from selenium.webdriver.common.by import By
import os, sys


"""Names files 0.png, 1.png, ..."""
def download_images(imgs: [], path: str, volume=1, name=1):

    for i in imgs:
        urllib.urlretrieve(i, os.path.join(path, str(volume) + '-' + str(name) + '.png'))
        name = name + 1

    urllib.urlcleanup()


"""Converts a list containing elements to a list containing the elements' specified attribute"""
def to_attribute_list(elements: [], attribute: str) -> list():

    attributes = []

    for i in elements:
        attributes.append(i.get_attribute(attribute))

    return attributes


"""Names directories 0, 1, 2, ... inside of a named directory if given or current directory by default"""
def create_directory(num=0, dirname='./') -> str:

    temp = "".join(i for i in dirname if i not in r"""<>:"/\|?*""")  # strip invalid characters

    if not os.path.exists(temp):
        os.makedirs(temp)

    return temp


def main():
    start=''
    numbertodownload=None
    try:
        start = sys.argv[1]
    except:
        print('ERROR: Requires URL as the first argument.', file=sys.stderr)
        quit(0)

    if len(sys.argv)>=3:
        numbertodownload = int(sys.argv[2])

    # Constants
    ALLDROPDOWN = '//*[@id="selectReadType"]/option[2]'
    ACTUALIMAGES = '//*[@id="divImage"]//img'
    IMGGROUPS = '.listing a'
    TITLE = '.bigChar'
    PAGEDROPDOWN = '#selectPage'

    wdo = webdriver.ChromeOptions()
    wdo.add_argument('--headless')
    wdo.add_argument('--disable-gpu')
    wdo.add_argument('log-level=2')
    # wdo.add_extension('C:/Webdrivers/extension_1_14_22.crx')

    # TODO: Create 'with' keyword webdriver __enter__ __exit__
    wd = webdriver.Chrome(chrome_options=wdo, desired_capabilities={'pageLoadStrategy':'none'})

    wait = WDW(wd, 10)

    wd.get(start)
    wait.until(EC.title_contains('manga'))  # wait a moment for javascript to process

    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, TITLE)))
    title = wd.find_element_by_css_selector(TITLE).text

    workingpath = create_directory(dirname=title[:25])

    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, IMGGROUPS)))
    groups = wd.find_elements_by_css_selector(IMGGROUPS)

    groups = to_attribute_list(groups, 'href')
    groups = list(reversed(groups))

    if numbertodownload:
        groups = [groups[numbertodownload-1]]

    for g in groups:
        wd.execute_script('''window.open("''' + g + '''","_blank");''')  # open a new tab
        wait.until(EC.number_of_windows_to_be(2))
        wd.switch_to.window(wd.window_handles[1])

        wait.until(EC.presence_of_element_located((By.XPATH, ALLDROPDOWN)))
        wd.find_element_by_xpath(ALLDROPDOWN).click()
        wait.until_not(EC.presence_of_element_located((By.CSS_SELECTOR, PAGEDROPDOWN)))  # wait for javascript

        wait.until(EC.presence_of_all_elements_located((By.XPATH, ACTUALIMAGES)))
        imgs = wd.find_elements_by_xpath(ACTUALIMAGES)

        wd.execute_script("window.stop();")  # stop loading the page

        download_images(to_attribute_list(imgs, 'src'), workingpath , volume=numbertodownload if numbertodownload else groups.index(g)+1)

        wd.execute_script('''window.close();''')
        wd.switch_to.window(wd.window_handles[0])

        print(str(groups.index(g)+1) + ' out of ' + str(len(groups)) + ' completed.')



main()
