import time
from bs4 import BeautifulSoup
from selenium import webdriver
from os import listdir, getcwd
from os.path import isfile, join, abspath
import openpyxl
from selenium.webdriver.firefox.options import Options
from enum import Enum



URL = "https://twitter.com/NRWINVESTRussia"
TAG = {"class": "css-4rbku5 css-18t94o4 css-901oao r-hkyrab r-1loqt21 r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-qvutc0"}
FILE = abspath("./../../Ziele_Marketing.xlsx")
# dirpath = getcwd()

class SocialMediaPositionInExcel(Enum):
    twitter = (11, 2)
    def __init__(self, row, column):
        self.row = row
        self.column = column


def getDataFromHtml(url, tag):
    options = Options()
    options.headless = True
    browser = webdriver.Firefox(options=options, executable_path=r'C:/Users/NRW Info/geckodriver.exe')
    browser.get(url)
    time.sleep(5) # js loading page waiting
    html = browser.page_source
    soup = BeautifulSoup(html, 'lxml')
    a = soup.findAll("a", tag)
    browser.quit()
    return a[1]['title'] #title attribute

     
def getXlsXFilePath():
    return [f for f in listdir(dirpath) if isfile(join(dirpath, f)) and f.endswith("test.xlsx") ]

# def addCellsWithValues(rowContent, ws, max):
#     print(rowContent)
#     for i, entry in enumerate(rowContent,start=1):
#         ws.cell(row=max+1, column=i+1, value=entry).border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))   

def writeToExel(data):
    wb = openpyxl.load_workbook(filename=FILE)
    ws = wb.active #todo unhardcode
    rowContent = data    
    ws.cell(row=SocialMediaPositionInExcel.twitter.row, column=SocialMediaPositionInExcel.twitter.column, value=rowContent)   
    wb.save(FILE)

def main():
    try:
        result = getDataFromHtml(URL, TAG)
        print(result)
    except Exception as err:
        print('parsing unsuccessfull', err)
   
    writeToExel(result)

if __name__ == "__main__":
    main()