import time
from bs4 import BeautifulSoup
from selenium import webdriver
from os import listdir, getcwd
from os.path import isfile, join, abspath
import openpyxl
from selenium.webdriver.firefox.options import Options
from enum import Enum

#todo 

URL_Twitter = "https://twitter.com/NRWINVESTRussia"
URL_Instagram = "https://www.instagram.com/nrw.invest_russia"
TAG_Twitter_ATTR = "css-4rbku5 css-18t94o4 css-901oao r-hkyrab r-1loqt21 r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-qvutc0"
TAG_Twitter = "a"
TAG_Twitter_Nth_Element = 1
TAG_Instagram = 'span'
TAG_Instagram_ATTR = 'g47SY' #class
TAG_Instagram_Nth_Element = 1 #second element
TAG_VK = 'span'
TAG_VK_ATTR = 'header_count fl_l'
TAG_VK_Nth_Element = 0
TAG_VK_SHOULD_GET_TEXT = True
URL_VK = 'https://vk.com/nrw.invest'

FILE = abspath("./Ziele_Marketing.xlsx")
#"./../../Ziele_Marketing.xlsx"
# dirpath = getcwd()

class SocialMediaEnum(Enum):
    twitter = (11, 2, TAG_Twitter, TAG_Twitter_ATTR, TAG_Twitter_Nth_Element, URL_Twitter)
    instagram = (11, 4, TAG_Instagram, TAG_Instagram_ATTR, TAG_Instagram_Nth_Element, URL_Instagram)
    vkontakte = (11, 8, TAG_VK, TAG_VK_ATTR, TAG_VK_Nth_Element, URL_VK, TAG_VK_SHOULD_GET_TEXT)
    def __init__(self, row, column, tag, tag_attr, tag_nth_element, url, tag_should_get_text =False ):
        self.row = row
        self.column = column
        self.tag = tag
        self.tag_attr = tag_attr
        self.tag_nth_element = tag_nth_element
        self.tag_should_get_text = tag_should_get_text
        self.url = url

def openBrowser():
    options = Options()
    options.headless = True
    browser = webdriver.Firefox(options=options, executable_path=r'C:/Users/Olga/Documents/geckodriver.exe')  #C:/Users/NRW Info/geckodriver.exe
    return browser

def getDataFromHtml(browser, social):
    browser.get(social.url)
    time.sleep(5) # js loading page waiting
    html = browser.page_source
    soup = BeautifulSoup(html, 'lxml')
    a = soup.findAll(social.tag, social.tag_attr)
    if social.tag_should_get_text == True:
        print(a[social.tag_nth_element].string)
        return a[social.tag_nth_element].get_text()
    else:
        print(a[social.tag_nth_element]['title'])
        return a[social.tag_nth_element]['title']

def getXlsXFilePath():
    return [f for f in listdir(dirpath) if isfile(join(dirpath, f)) and f.endswith("test.xlsx") ]

def writeToExel(data, social, worksheet):
    worksheet.cell(row=social.row, column=social.column, value=data)

def main():
    browser = openBrowser()
    wb = openpyxl.load_workbook(filename=FILE)
    worksheet = wb.active #todo unhardcode
    for social in SocialMediaEnum:
        try:
            print(social.url, social.tag)  #debugging    
            result = getDataFromHtml(browser, social)
            print(result)
            writeToExel(result, social, worksheet)
        except Exception as err:
            print('parsing unsuccessfull', err)
    browser.quit()
    wb.save(FILE)


if __name__ == "__main__":
    main()