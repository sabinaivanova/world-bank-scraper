from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import json

#webdriver path
driver = webdriver.Chrome(r'C:\Users\...\chromedriver.exe')

#open link to articles related to Bulgaria
worldBankUrl = 'https://datacatalog.worldbank.org/search?sort_by=field_wbddh_modified_date&sort_order=DESC&f%5B0%5D=field_wbddh_country%3A67&q=search&page=0%2C0'
driver.get(worldBankUrl)
driver.maximize_window()

urls = []

#scrape urls of articles
def scrape_urls():
    content = driver.find_element_by_class_name('view-content')
    articleUrls = len(content.find_elements_by_class_name('node-title'))
    for i in range(1, articleUrls + 1):
        article = '/html/body/div[4]/div/div/div[3]/section/div/div/div[2]/div[2]/div[2]/div/div/div[3]/div/div/div[2]/div['
        article += str(i)
        article += ']/div/h2/a'
        driver.implicitly_wait(2)
        articleUrl = driver.find_element_by_xpath(article).get_attribute('href')
        
        #append urls to a list
        urls.append(articleUrl)
        
        #append url list to nested dicts
        nestedDict = {"url": urls}        
        mainDict = {"Articles Bulgaria": nestedDict}
        
        #write data to json
        with open("wb_bulgaria_article_urls_2020_08_06_ss.json", "w", encoding = "utf-8") as g:
            json.dump(mainDict, g, skipkeys = True, indent = 4)

#go through all pages to scrape urls
while True:
    try: 
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        nextB = driver.find_element_by_class_name('pager-next')
        nextButton = nextB.find_element_by_tag_name('a').get_attribute('href')
        driver.implicitly_wait(3)
        driver.get(nextButton)
        driver.implicitly_wait(2)
        scrape_urls()
    except NoSuchElementException:
        driver.quit()
        print("Article URL download complete")
