import time
from bs4 import BeautifulSoup
from selenium import webdriver

url = "https://twitter.com/NRWINVESTRussia"
browser = webdriver.Firefox(executable_path=r'C:\Users\NRW Info\geckodriver.exe')
browser.get(url)
time.sleep(10) # js loading page
html = browser.page_source
soup = BeautifulSoup(html, 'lxml')
a = soup.findAll("a", {"class": "css-4rbku5 css-18t94o4 css-901oao r-hkyrab r-1loqt21 r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-qvutc0"})

print(a[1]['title']) #title attribute